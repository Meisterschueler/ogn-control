import enum


class TakeoffLanding():
    def __init__(self, address, timestamp, is_takeoff):
        self.address = address
        self.timestamp = timestamp
        self.is_takeoff = is_takeoff


class State(enum.Enum):
    UNKNOWN, GROUND, MOVING, STARTING, AIRBORNE, LANDING, \
        ABORTING_START, ABORTING_LANDING = range(8)


class StateMachine():
    def __init__(self, elevation=0, max_last_messages=10):
        self.elevation = elevation
        self.max_last_messages = max_last_messages

        self.aircrafts = {}
        self.takeoff_landings = []

    def add_message(self, message):
        address = message['address']
        if address not in self.aircrafts:
            self.aircrafts[address] = {'state': State.UNKNOWN, 'messages': [message]}
            return

        last_state = self.aircrafts[address]['state']
        last_message = self.aircrafts[address]['messages'][-1]
        last_ground_speed = last_message['ground_speed']
        last_altitude = last_message['altitude']

        ground_speed = message['ground_speed']
        altitude = message['altitude']

        min_airborne_altitude = self.elevation + 200
        min_moving_speed = 10
        min_airborne_speed = 30

        if last_state == State.UNKNOWN:
            if last_ground_speed < min_moving_speed and last_altitude < min_airborne_altitude:
                if ground_speed < min_moving_speed and altitude < min_airborne_altitude:
                    state = State.GROUND
                elif ground_speed < min_airborne_speed and altitude < min_airborne_altitude:
                    state = State.MOVING
                else:
                    state = State.UNKNOWN
            elif last_ground_speed >= min_airborne_speed and last_altitude >= min_airborne_altitude:
                if ground_speed >= min_airborne_speed and altitude >= min_airborne_altitude:
                    state = State.AIRBORNE
                else:
                    state = State.UNKNOWN
            else:
                state = State.UNKNOWN
        elif last_state == State.GROUND:
            if ground_speed < min_moving_speed and altitude < min_airborne_altitude:
                state = State.GROUND
            elif ground_speed < min_airborne_speed and altitude < min_airborne_altitude:
                state = State.MOVING
            elif altitude < min_airborne_altitude:
                state = State.STARTING
            else:
                state = State.UNKNOWN
        elif last_state == State.MOVING:
            if ground_speed < min_moving_speed and altitude < min_airborne_altitude:
                state = State.GROUND
            elif ground_speed < min_airborne_speed and altitude < min_airborne_altitude:
                state = State.MOVING
            elif altitude < min_airborne_altitude:
                state = State.STARTING
            else:
                state = State.UNKNOWN
        elif last_state == State.STARTING:
            if ground_speed >= min_airborne_speed and altitude < min_airborne_altitude:
                state = State.STARTING
            elif ground_speed >= min_airborne_speed and altitude >= min_airborne_altitude:
                state = State.AIRBORNE
            elif ground_speed < min_airborne_altitude and altitude < min_airborne_altitude:
                state = State.ABORTING_START
            else:
                state = State.UNKNOWN
        elif last_state == State.AIRBORNE:
            if ground_speed >= min_airborne_speed and altitude >= min_airborne_altitude:
                state = State.AIRBORNE
            elif ground_speed >= min_airborne_speed and altitude < min_airborne_altitude:
                state = State.LANDING
            else:
                state = State.UNKNOWN
        elif last_state == State.LANDING:
            if ground_speed >= min_airborne_speed and altitude < min_airborne_altitude:
                state = State.LANDING
            elif ground_speed < min_airborne_speed and ground_speed >= min_moving_speed and altitude < min_airborne_altitude:
                state = State.MOVING
            else:
                state = State.UNKNOWN
        elif last_state == State.ABORTING_START:
            if ground_speed < min_moving_speed and altitude < min_airborne_altitude:
                state = State.GROUND
            elif ground_speed < min_airborne_speed and altitude < min_airborne_altitude:
                state = State.MOVING
            else:
                state = State.UNKNOWN
        else:
            state = State.UNKNOWN

        if last_state == State.STARTING and state == State.AIRBORNE:
            print("Started: {}".format(message))
            takeoff = TakeoffLanding(address=message['address'], timestamp=message['timestamp'], is_takeoff=True)
            self.takeoff_landings.append(takeoff)
        elif last_state == State.LANDING and state == State.MOVING:
            print("Landed: {}".format(message))
            landing = TakeoffLanding(address=message['address'], timestamp=message['timestamp'], is_takeoff=False)
            self.takeoff_landings.append(landing)

        self.aircrafts[address]['state'] = state
        self.aircrafts[address]['messages'].append(message)

    def get_state(self, address):
        return self.aircrafts[address]['state'] if address in self.aircrafts else None
