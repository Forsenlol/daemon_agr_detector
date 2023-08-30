import os

import dlib
import imutils.face_utils
import numpy as np
import torch


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if torch.cuda.is_available():
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
else:
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

base_path = 'models/'  # os.path.dirname(os.path.abspath(__file__))
PREDICTOR_PATH = os.path.join(base_path, "shape_predictor_5_face_landmarks.dat")
CNN_FACE_DETECTOR_PATH = os.path.join(base_path, 'mmod_human_face_detector.dat')

MODEL_PATH = os.path.join(base_path, 'hf_race_gender_and_age_arabian_v1_1.pt')

races_values = ['african', 'arabian', 'asian', 'caucasian', 'hispanic', 'indian']

stats_mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
stats_std = np.array([0.229, 0.224, 0.225], dtype=np.float32)

print('CNN_FACE_DETECTOR_PATH', CNN_FACE_DETECTOR_PATH)
detector = dlib.cnn_face_detection_model_v1(CNN_FACE_DETECTOR_PATH)
predictor = dlib.shape_predictor(PREDICTOR_PATH)

face_aligner = imutils.face_utils.FaceAligner(predictor, desiredLeftEye=(0.3, 0.3), desiredFaceWidth=224)

MODEL_SOURCE_FULL_NAME = 'full_name'
MODEL_SOURCE_ALPHABET = 'alphabet'

models = {
    'age_model': None,
    'gender_model': None,
    'genders': None,
    'race_model': None,
    'races': None,
}
