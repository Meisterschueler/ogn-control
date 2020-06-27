import unittest
from datetime import datetime

from app.staterecognition import StateMachine, State


class Test(unittest.TestCase):
    def test_simple_takeoff(self):
        messages = [
            {'timestamp': datetime(2020, 6, 27, 10, 30,  0), 'address': 'DD1234', 'ground_speed':  0.0, 'altitude': 600, 'climb_rate': 0.0, 'track': 90.0},
            {'timestamp': datetime(2020, 6, 27, 10, 30, 10), 'address': 'DD1234', 'ground_speed':  0.0, 'altitude': 600, 'climb_rate': 0.0, 'track': 90.0},
            {'timestamp': datetime(2020, 6, 27, 10, 30, 20), 'address': 'DD1234', 'ground_speed': 10.0, 'altitude': 600, 'climb_rate': 0.0, 'track': 90.0},
            {'timestamp': datetime(2020, 6, 27, 10, 30, 30), 'address': 'DD1234', 'ground_speed': 50.0, 'altitude': 600, 'climb_rate': 0.0, 'track': 90.0},
            {'timestamp': datetime(2020, 6, 27, 10, 30, 40), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 600, 'climb_rate': 0.0, 'track': 90.0},
            {'timestamp': datetime(2020, 6, 27, 10, 30, 50), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 650, 'climb_rate': 5.0, 'track': 90.0},
            {'timestamp': datetime(2020, 6, 27, 10, 31,  0), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 700, 'climb_rate': 5.0, 'track': 90.0},
            {'timestamp': datetime(2020, 6, 27, 10, 31, 10), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 750, 'climb_rate': 5.0, 'track': 90.0},
            {'timestamp': datetime(2020, 6, 27, 10, 31, 20), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 800, 'climb_rate': 5.0, 'track': 90.0},
            {'timestamp': datetime(2020, 6, 27, 10, 31, 30), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 850, 'climb_rate': 5.0, 'track': 90.0},
            {'timestamp': datetime(2020, 6, 27, 10, 31, 40), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 900, 'climb_rate': 5.0, 'track': 90.0},
            {'timestamp': datetime(2020, 6, 27, 10, 31, 50), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 950, 'climb_rate': 5.0, 'track': 90.0},
        ]

        state_machine = StateMachine(elevation=600)

        state_machine.add_message(messages[0])
        state = state_machine.get_state(address='DD1234')
        self.assertEqual(state, State.UNKNOWN)

        state_machine.add_message(messages[1])
        state = state_machine.get_state(address='DD1234')
        self.assertEqual(state, State.GROUND)

        state_machine.add_message(messages[2])
        state = state_machine.get_state(address='DD1234')
        self.assertEqual(state, State.MOVING)

        for message in messages[3:7]:
            state_machine.add_message(message)
        state = state_machine.get_state(address='DD1234')
        self.assertEqual(state, State.STARTING)

        for message in messages[7:]:
            state_machine.add_message(message)
        state = state_machine.get_state(address='DD1234')
        self.assertEqual(state, State.AIRBORNE)
