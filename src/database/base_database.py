import pymongo
import os

import pymongo.errors

from src.utils.logger import logging
from src.config.app_config import Config as cfg


class BaseDatabase(object):
    def __init__(self, config):
        self.host_name = config['hostname']
        self.port = config['port']
        self.user = cfg.DATABASE_USER
        self.password = cfg.DATABASE_PASSWORD
        if (self.user == None or self.password == None) or (self.user == '' or self.password == ''):
            self.url = f"mongodb://{self.host_name}:{self.port}"
        else:
            self.url = f"mongodb://{self.user}:{self.password}@{self.host_name}:{self.port}"

        self.initialize()
    

    def initialize(self):
        try:
            self.client = pymongo.MongoClient(self.url)
            logging.info("Connected to database")
        except pymongo.errors.ServerSelectionTimeoutError as e:
            logging.error(f"Error connecting to database: {e}")
            raise e