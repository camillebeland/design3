from flask import Flask, render_template
from configuration import configuration

app = Flask(__name__, static_folder='webapp/static', template_folder='webapp/templates')


@app.route('/')
def index():
    return render_template("index.html")


def start_server(port):
    app.run(port=port)


if __name__ == '__main__':
    config = configuration.getconfig()
    port = int(config.get('webapp', 'port'))
    start_server(port)

