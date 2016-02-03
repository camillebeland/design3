import configparser

def getconfig():
    print("Reading configuration file")
    config = configparser.ConfigParser()
    config.read('project.cfg')
    config.get('robot', 'port')
    return config
