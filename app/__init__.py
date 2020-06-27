import os
from datetime import timezone

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_bootstrap import Bootstrap

from ogn.client.client import TelnetClient
from ogn.parser.telnet_parser import parse

from config import configs
from app.staterecognition import StateMachine


# Create the app
app = Flask(__name__)

# Load the configuration
config_name = app.config['ENV']
configuration = configs[config_name]
app.config.from_object(configuration)

socketio = SocketIO(app)
bootstrap = Bootstrap(app)

thread = None


here = os.path.dirname(os.path.realpath(__file__))
state_machine = StateMachine(elevation=app.config['ELEVATION'])


def emit_test_data():
    """Emits test data from static file for testing purposes."""

    timestamp = None

    for line in open(os.path.join(here, "telnet_logfile.txt")):
        raw_message = line.rstrip("\n")
        message = parse(raw_message)

        if not message:
            if not raw_message.startswith('APRS'):
                print("Could not parse: {}".format(raw_message))
            continue

        state_machine.add_message(message)
        message["timestamp"] = int(message["timestamp"].replace(tzinfo=timezone.utc).timestamp())

        if timestamp is None:
            timestamp = message["timestamp"]

        socketio.emit("ogn_data", message, namespace="/ogn")
        if timestamp != message["timestamp"]:
            timestamp = message["timestamp"]
            socketio.sleep(1.0)


def emit_realtime_data():
    """Connects with telnet client and emit realtime data."""

    def callback(raw_message):
        message = parse(raw_message)
        if not message:
            if not raw_message.startswith('APRS'):
                print("Could not parse: {}".format(raw_message))
            return

        state_machine.add_message(message)
        message["timestamp"] = int(message["timestamp"].replace(tzinfo=timezone.utc).timestamp())
        socketio.emit("ogn_data", message, namespace="/ogn")

    client = TelnetClient()
    client.connect()
    client.run(callback=callback)


@socketio.on("connect", namespace="/ogn")
def client_connect():
    global thread
    if thread is None:
        if app.config['DEBUG']:
            thread = socketio.start_background_task(target=emit_test_data)
        else:
            thread = socketio.start_background_task(target=emit_realtime_data)
    emit("server_response", {"data": "Connected", "count": 0})


@app.route("/")
@app.route("/flot.html")
def flot():
    return render_template("flot.html",
                           title="Flot")


@app.route("/plotly.html")
def plotly():
    return render_template("plotly.html",
                           title="Plotly")


@app.route("/messages.html")
def messages():
    return render_template("messages.html",
                           title="Messages")


@app.route("/logbook.html")
def logbook():
    return render_template("logbook.html",
                           title="Logbook",
                           logbook=state_machine.takeoff_landings)
