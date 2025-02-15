import os

from dotenv import load_dotenv

from src.utils.common import read_yaml_file
from src.utils.logger import logging
from src.config import *

load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    RUNPOD_TOKEN = os.getenv("RUNPOD_TOKEN")
    RUNPOD_URL = os.getenv("RUNPOD_URL")

    DATABASE_URL = os.getenv("DATABASE_URL")
    DATABASE_HOSTNAME = os.getenv("DATABASE_HOSTNAME")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")


class CryptoConfig:
    cfg = read_yaml_file(CRYPTO_CFG_FILE_PATH)

    agent_cfg = cfg['agent']
    common_cfg = cfg['common']

    model = agent_cfg['model']
    chatbot_model_name = agent_cfg['chatbot_model_name']
    rate_limit_delay = agent_cfg['rate_limit_delay']
    temperature = agent_cfg['temperature']
    top_p = agent_cfg['top_p']
    max_tokens = agent_cfg['max_tokens']
    
    data_path = common_cfg['data_path']
    wallet_age_report_path = common_cfg['wallet_age_report_path']
    trend_analysis_report_path = common_cfg['trend_analysis_report_path']
    transaction_analysis_report_path = common_cfg['transaction_analysis_report_path']
    behavioral_classification_path = common_cfg['behavioral_classification_path']
    etherscan_base_url= common_cfg['etherscan_base_url']

    

class DatabaseConfig:
    def __init__(self):
        self.config = read_yaml_file(DATABASE_CFG_FILE_PATH)
        logging.info('Init Crypto Database configuration parameters')

    def init_database(self):
        return self.config['crypto_database']
    