import yaml
import logging
import logging.config
import os


def load_config():
    config_filename = 'configuration/config.yaml'

    # Attempt to load configuration file from user's home directory
    config_path = os.path.join(os.path.abspath(os.getcwd()), config_filename)

    try:
        config = yaml.safe_load(open(config_path))
    except IOError:
        logging.ERROR(f'No es posible cargar el {config_filename}')

    # Verify classes API
    if 'API_KEY' not in config:
        logging.ERROR(f'Please set Classes API key as "api key" in {config_filename}.')
        return None
    return config
