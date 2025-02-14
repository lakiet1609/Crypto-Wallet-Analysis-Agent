import yaml
from src.utils.logger import logging


def read_yaml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)  
        return data
    except FileNotFoundError:
        logging.info(f"Error: The file {file_path} was not found.")
    except yaml.YAMLError as exc:
        logging.info(f"Error parsing YAML file: {exc}")
    except Exception as e:
        logging.info(f"An error occurred: {e}")
