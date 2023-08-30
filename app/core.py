import logging
import base64
import datetime
from collections import Counter

import numpy as np
import torch
import cv2

from app.alphabet_detector import get_alphabets
from config import (
    detector,
    device,
    face_aligner,
    stats_mean,
    stats_std,
    races_values,
    MODEL_SOURCE_FULL_NAME,
    MODEL_SOURCE_ALPHABET,
    models,
)
from sexmachine.auditor_gender import get_auditor_gender


def detect_full_names_gender(data: dict):
    result = []
    if 'full_names' in data:
        for item in data['full_names']:
            result.append({
                'id': item['id'],
                'gender': get_auditor_gender(item['full_name']),
            })

    return result


def load_image(imn):
    return cv2.cvtColor(cv2.imread(imn), cv2.COLOR_BGR2RGB)


def decode_image(data):
    return cv2.cvtColor(cv2.imdecode(data), cv2.COLOR_BGR2RGB)


def detect_faces(img):
    return detector(img, 1)


def align_face(img, face_rect):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return face_aligner.align(img, gray, face_rect)


def load_models(path):
    if device.type == 'cpu':
        logging.info(f'Load model: {path} on CPU')
        bundle = torch.load(path, map_location='cpu')
    else:
        logging.info(f'Load model: {path} on CUDA')
        bundle = torch.load(path, map_location='cuda')
    return bundle['age_model'], bundle['gender_model'], bundle['genders'], bundle['race_model'], bundle['races']


def transform_image(img):
    return np.rollaxis(((cv2.resize(img, (224, 224)).astype(np.float32) / 255.0 - stats_mean) / stats_std), 2)


def detect_age_and_race_raw(imgs):
    with torch.no_grad():
        if device.type == 'cpu':
            inp = torch.FloatTensor(imgs).cpu()
        else:
            inp = torch.FloatTensor(imgs).cuda()
        return (
            models['age_model'](inp).cpu().numpy(),
            models['gender_model'](inp).cpu().numpy(),
            models['race_model'](inp).cpu().numpy(),
        )


def core_predict(item: dict):
    result = {
        'id': item['id']
    }

    if 'full_name' in item and 'id' in item:
        gender, gender_source = get_auditor_gender(str(item['id']), str(item['full_name']))
        if gender != 'unknown':
            result['gender'] = gender
            result['gender_source'] = MODEL_SOURCE_FULL_NAME
            result['gender_info'] = gender_source
    if 'texts' in item:
        alphabets: Counter = get_alphabets(item['texts'])
        if len(alphabets) > 0:
            arabic_counter = sum(alphabets[alphabet] for alphabet in alphabets if alphabet in ['ARABIC', 'HEBREW'])
            asian_counter = sum(
                alphabets[alphabet] for alphabet in alphabets if alphabet in ['CJK', 'HANGUL', 'HIRAGANA', 'KATAKANA', 'THAI'])
            if arabic_counter >= 2:
                result['race'] = 'arabian'
                result['race_source'] = MODEL_SOURCE_ALPHABET
            elif asian_counter >= 2:
                result['race'] = 'asian'
                result['race_source'] = MODEL_SOURCE_ALPHABET
    if 'image' in item:
        try:
            bin_data = base64.b64decode(item['image'])
        except ValueError:
            result['error'] = 'bad base64 image for id: {}'.format(item['id'])
            logging.error(result['error'])
            return result
        img = cv2.imdecode(np.frombuffer(bin_data, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            return result
        if img.shape[0] > 150 or img.shape[1] > 150:
            img = cv2.resize(img, (150, 150))
        if img.shape[0] < 64 or img.shape[1] < 64:
            return result
        faces = detect_faces(img)
        if faces is None or len(faces) < 1:
            return result

        face_rect = faces[0].rect
        aligned_face = align_face(img, face_rect)
        tfmd_face = transform_image(aligned_face)

        age_pred, gender_pred, race_pred = detect_age_and_race_raw(tfmd_face[None])

        if 'race' not in result:
            result['race'] = races_values[race_pred.argmax()]
            result['race_source'] = 'hypeauditor_model'
            result['race_pred'] = race_pred[0].tolist()

        result['year'] = datetime.datetime.now().year - int(age_pred[0][0] + item['age_corr'])
        result['year_source'] = 'hypeauditor_model'
        result['age'] = int(age_pred[0][0] + item['age_corr'])

        if 'gender' not in result:
            result['gender'] = models['genders'][gender_pred[0].argmax()]
            result['gender_source'] = 'hypeauditor_model'
        result['gender_by_photo'] = models['genders'][gender_pred[0].argmax()]
        result['gender_pred'] = gender_pred[0].tolist()
        result['model_version'] = 'hypeauditor_model'
        result['faces_count'] = len(faces)

        del faces
        del [face_rect, age_pred, gender_pred, race_pred, tfmd_face, aligned_face]

    return result
