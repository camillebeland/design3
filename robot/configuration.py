from getopt import getopt

class Parser:
    def __init__(self, args):
        self.options, self.args= getopt(args, 'p:', ['port='])
        for key, value in self.options:
            if(key in ('-p', '--port')):
                self.port = int(value)

    def get_option(self, option_name):
        if(option_name == 'port'):
            return self.port or 5000
