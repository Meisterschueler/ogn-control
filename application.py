from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
bootstrap = Bootstrap(app)
nav = Nav()

thread = None

from ogn.client.client import TelnetClient
from ogn.parser.telnet_parser import parse

from datetime import timezone


def background_thread2():
    data_strings = [line.rstrip('\n') for line in open('output.txt')]

    while True:
        for raw_message in data_strings:
            message = parse(raw_message)
            if not message:
                print('Could not parse %s' % raw_message)
                continue

            message['timestamp'] = int(message['timestamp'].replace(tzinfo=timezone.utc).timestamp())
            socketio.emit('ogn_data', message, namespace='/test')
            socketio.sleep(0.1)


def background_thread():
    def callback(raw_message):
        message = parse(raw_message)
        if not message:
            print('Could not parse %s' % raw_message)
            return

        socketio.emit('ogn_data', message, namespace='/test')

    client = TelnetClient()
    client.connect()
    client.run(callback=callback)


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread2)
    emit('my_response', {'data': 'Connected', 'count': 0})


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.jinja')


@app.route('/config.html')
def config():
    return render_template('config.jinja')


@app.route('/thisnthat.html')
def thisnthat():
    return render_template('thisnthat.jinja')


@nav.navigation()
def mynavbar():
    return Navbar(
        'OGN Receiver',
        View('Home', 'index'),
        View('Configuration', 'config'),
        View('Thisnthat', 'thisnthat'),
    )

nav.init_app(app)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
