from configuration import configuration
from webapp import server

if __name__ == '__main__':
    config = configuration.getconfig()
    port = int(config.get('webapp', 'port'))
    server.run(port)
