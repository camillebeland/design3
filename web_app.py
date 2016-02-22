from configuration import configuration
from webapp import server

if __name__ == '__main__':
    config = configuration.getconfig()
    host = config.get('webapp', 'host')
    port = config.getint('webapp', 'port')
    server.run(host, port)
