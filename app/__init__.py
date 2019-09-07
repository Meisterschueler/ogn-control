import os
from datetime import timezone

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_bootstrap import Bootstrap

from ogn.client.client import TelnetClient
from ogn.parser.telnet_parser import parse


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)
bootstrap = Bootstrap(app)

thread = None


mypath = os.path.dirname(os.path.realpath(__file__))


def emit_test_data():
    """Emits test data from static file for testing purposes."""
    
    data_strings = [line.rstrip("\n") for line in open(os.path.join(mypath, "telnet_logfile.txt"))]
    timestamp = None

    for raw_message in data_strings:
        message = parse(raw_message)

        if not message:
            continue

        message["timestamp"] = int(message["timestamp"].replace(tzinfo=timezone.utc).timestamp())

        if timestamp is None:
            timestamp = message["timestamp"]

        socketio.emit("ogn_data", message, namespace="/test")
        if timestamp != message["timestamp"]:
            timestamp = message["timestamp"]
            socketio.sleep(1.0)


def emit_real_data():
    """Connects with telnet client and emit 'real' data."""
    
    def callback(raw_message):
        message = parse(raw_message)
        if not message:
            print("Could not parse %s" % raw_message)
            return

        socketio.emit("ogn_data", message, namespace="/test")

    client = TelnetClient()
    client.connect()
    client.run(callback=callback)


@socketio.on("connect", namespace="/test")
def test_connect():
    global thread
    if thread is None:
        if app.config['DEBUG']:
            thread = socketio.start_background_task(target=emit_test_data)
        else:
            thread = socketio.start_background_task(target=emit_real_data)
    emit("my_response", {"data": "Connected", "count": 0})


@app.route("/")
@app.route("/flot.html")
def flot():
    return render_template("flot.html", title="Flot")


@app.route("/plotly.html")
def plotly():
    return render_template("plotly.html", title="Plotly")


@app.route("/messages.html")
def messages():
    return render_template("messages.html", title="Messages")

@app.route("/fullscreen.html")
def fullscreen():
    return render_template("fullscreen.html", title="Fullscreen")
