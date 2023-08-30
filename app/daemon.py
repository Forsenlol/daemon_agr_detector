import logging
import os
from time import perf_counter

from flask import request, jsonify
from flask_restx import Namespace
from flask_restx import Resource

from app import core

ns = Namespace('AGR Detector', description='AGR Detector Api', path='/')


@ns.route('/predict')
class PredictHandler(Resource):
    def post(self):
        logging.info('Request: {}, {} MB'.format(
            request.content_type, round(request.content_length / 1024 / 1024, 2))
        )
        input: dict = request.get_json(force=True)
        result = []

        images = input['input']
        logging.info('Try to detect {} images, first id: {}'.format(len(images), images[0]['id']))
        time_start = perf_counter()

        detected_count = 0
        for item in images:
            predict_result = core.core_predict(item)
            # эта проверка не работает, он там нан не возвращает
            if predict_result is not None:
                result.append(predict_result)
                # там всегда возвращает айди канала, но если что-то задетектили - будут доп поля, их и ловим
                if len(predict_result) > 1:
                    detected_count += 1

        logging.info('Processed {} of {} images in {} seconds'.format(
            detected_count, len(images), round(perf_counter() - time_start, 2))
        )

        return jsonify({
            'status': 'ok',
            'result': result
        })
