import unittest
from datetime import datetime

from app.staterecognition import StateMachine, State


class Test(unittest.TestCase):
    def test_simple_takeoff(self):
        messages = [
            {'expected_state': State.UNKNOWN, ' timestamp': datetime(2020, 6, 27, 10, 30,  0), 'address': 'DD1234', 'ground_speed':  0.0, 'altitude': 600, 'climb_rate': 0.0, 'track': 90.0},
            {'expected_state': State.GROUND,   'timestamp': datetime(2020, 6, 27, 10, 30, 10), 'address': 'DD1234', 'ground_speed':  0.0, 'altitude': 600, 'climb_rate': 0.0, 'track': 90.0},
            {'expected_state': State.MOVING,   'timestamp': datetime(2020, 6, 27, 10, 30, 20), 'address': 'DD1234', 'ground_speed': 10.0, 'altitude': 600, 'climb_rate': 0.0, 'track': 90.0},
            {'expected_state': State.STARTING, 'timestamp': datetime(2020, 6, 27, 10, 30, 30), 'address': 'DD1234', 'ground_speed': 50.0, 'altitude': 600, 'climb_rate': 0.0, 'track': 90.0},
            {'expected_state': State.STARTING, 'timestamp': datetime(2020, 6, 27, 10, 30, 40), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 600, 'climb_rate': 0.0, 'track': 90.0},
            {'expected_state': State.STARTING, 'timestamp': datetime(2020, 6, 27, 10, 30, 50), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 650, 'climb_rate': 5.0, 'track': 90.0},
            {'expected_state': State.STARTING, 'timestamp': datetime(2020, 6, 27, 10, 31,  0), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 700, 'climb_rate': 5.0, 'track': 90.0},
            {'expected_state': State.STARTING, 'timestamp': datetime(2020, 6, 27, 10, 31, 10), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 750, 'climb_rate': 5.0, 'track': 90.0},
            {'expected_state': State.AIRBORNE, 'timestamp': datetime(2020, 6, 27, 10, 31, 20), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 800, 'climb_rate': 5.0, 'track': 90.0},
            {'expected_state': State.AIRBORNE, 'timestamp': datetime(2020, 6, 27, 10, 31, 30), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 850, 'climb_rate': 5.0, 'track': 90.0},
            {'expected_state': State.AIRBORNE, 'timestamp': datetime(2020, 6, 27, 10, 31, 40), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 900, 'climb_rate': 5.0, 'track': 90.0},
            {'expected_state': State.AIRBORNE, 'timestamp': datetime(2020, 6, 27, 10, 31, 50), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 950, 'climb_rate': 5.0, 'track': 90.0},
        ]

        state_machine = StateMachine(elevation=600)

        for message in messages:
            state_machine.add_message(message)
            self.assertEqual(message['expected_state'], state_machine.get_state(address='DD1234'))
