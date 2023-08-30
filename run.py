import os
import logging

import faulthandler
import torch
from flask import Flask
from flask_restx import Api

from app.daemon import ns
from app.core import load_models
from config import models, MODEL_PATH, device


def create_app():
    print('Create APP/API')
    app = Flask(__name__)
    api = Api(
        title='data api IG',
        version='1.0',
        description='Data api IG',
        prefix="/api"
    )
    api.add_namespace(ns)
    api.init_app(app)

    print('faulthandler.enable()')
    faulthandler.enable()

    print(f'Device: {device.type}')

    print('Load model in progress...')
    models['age_model'], models['gender_model'], models['genders'], models['race_model'], models['races'] = (
        load_models(MODEL_PATH)
    )

    print('Run app')
    return app


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run()
