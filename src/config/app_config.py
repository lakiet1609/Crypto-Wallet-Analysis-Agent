import os

from dotenv import load_dotenv

from src.utils.common import read_yaml_file
from src.utils.logger import logging
from src.config import *

load_dotenv()


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    DATABASE_HOSTNAME = os.getenv("DATABASE_HOSTNAME")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")


class DatabaseConfig:
    def __init__(self):
        self.config = read_yaml_file(DATABASE_CFG_FILE_PATH)
        logging.info('Init Crypto Database configuration parameters')

    def init_database(self):
        return self.config['crypto_database']