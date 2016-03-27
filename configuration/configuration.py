import configparser
import os


def get_config():
    print("Reading configuration file")
    config = configparser.ConfigParser()

    base_directory = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(base_directory, 'project.cfg')
    config_file = open(config_path)
    config.read_file(config_file)

    config.get('robot', 'port')
    return config
