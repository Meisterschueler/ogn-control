import enum


class State(enum.Enum):
    UNKNOWN, GROUND, MOVING, STARTING, AIRBORNE, LANDING = range(6)


class StateMachine():
    aircrafts = {}

    def __init__(self, elevation=0, max_last_messages=10):
        self.elevation = elevation
        self.max_last_messages = max_last_messages

    def add_message(self, message):
        address = message['address']
        if address not in self.aircrafts:
            self.aircrafts[address] = {'state': State.UNKNOWN, 'messages': []}
            self.aircrafts[address]['messages'].append(message)
            return

        last_state = self.aircrafts[address]['state']
        last_message = self.aircrafts[address]['messages'][-1]
        last_ground_speed = last_message['ground_speed']
        last_altitude = last_message['altitude']

        ground_speed = message['ground_speed']
        altitude = message['altitude']

        min_airborne_altitude = self.elevation + 200
        min_moving_speed = 10
        min_starting_speed = 30

        if last_state == State.UNKNOWN and last_ground_speed < 10 and last_altitude < min_airborne_altitude:
            if ground_speed < min_moving_speed and altitude < min_airborne_altitude:
                state = State.GROUND
            elif ground_speed < min_starting_speed and altitude < min_airborne_altitude:
                state = State.MOVING
            else:
                state = State.UNKNOWN
        elif last_state == State.GROUND:
            if ground_speed < min_moving_speed and altitude < min_airborne_altitude:
                state = State.GROUND
            elif ground_speed < min_starting_speed and altitude < min_airborne_altitude:
                state = State.MOVING
            elif altitude < min_airborne_altitude:
                state = State.STARTING
            else:
                state = State.UNKNOWN
        elif last_state == State.MOVING:
            if ground_speed < min_moving_speed and altitude < min_airborne_altitude:
                state = State.GROUND
            elif ground_speed < min_starting_speed and altitude < min_airborne_altitude:
                state = State.MOVING
            elif altitude < min_airborne_altitude:
                state = State.STARTING
            else:
                state = State.UNKNOWN
        elif last_state == State.STARTING:
            if ground_speed >= min_starting_speed and altitude < min_airborne_altitude:
                state = State.STARTING
            elif ground_speed >= min_starting_speed and altitude >= min_airborne_altitude:
                state = State.AIRBORNE
            else:
                state = State.UNKNOWN
        elif last_state == State.AIRBORNE:
            state = State.AIRBORNE
        else:
            state = State.UNKNOWN

        self.aircrafts[address]['state'] = state
        self.aircrafts[address]['messages'].append(message)

    def get_state(self, address):
        return self.aircrafts[address]['state'] if address in self.aircrafts else None
