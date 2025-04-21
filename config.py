import os


class Config:
    # Flask конфігурація
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')

    # MongoDB конфігурація
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'library_service')