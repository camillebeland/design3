from configuration import configuration
from webapp import server


def run():
    config = configuration.get_config()
    host = config.get('webapp', 'host')
    port = config.getint('webapp', 'port')
    server.run(host, port)


if __name__ == '__main__':
    run()



