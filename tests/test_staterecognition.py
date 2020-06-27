import unittest
from datetime import datetime

from app.staterecognition import StateMachine, State


class Test(unittest.TestCase):
    def test_simple_takeoff(self):
        """One plane makes one takeoff."""

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

            state = state_machine.get_state(address='DD1234')
            expected_state = message['expected_state']
            self.assertEqual(expected_state, state)

        takeoff_landings = state_machine.takeoff_landings
        self.assertEqual(len(takeoff_landings), 1)
        self.assertEqual(takeoff_landings[0].address, 'DD1234')
        self.assertEqual(takeoff_landings[0].timestamp, datetime(2020, 6, 27, 10, 31, 20))
        self.assertTrue(takeoff_landings[0].is_takeoff)

    def test_simple_landing(self):
        """One plane makes one landing."""

        messages = [
            {'expected_state': State.UNKNOWN,  'timestamp': datetime(2020, 6, 27, 10, 30,  0), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 950, 'climb_rate': -5.0, 'track': 90.0},
            {'expected_state': State.AIRBORNE, 'timestamp': datetime(2020, 6, 27, 10, 30, 10), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 900, 'climb_rate': -5.0, 'track': 90.0},
            {'expected_state': State.AIRBORNE, 'timestamp': datetime(2020, 6, 27, 10, 30, 20), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 850, 'climb_rate': -5.0, 'track': 90.0},
            {'expected_state': State.AIRBORNE, 'timestamp': datetime(2020, 6, 27, 10, 30, 30), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 800, 'climb_rate': -5.0, 'track': 90.0},
            {'expected_state': State.LANDING,  'timestamp': datetime(2020, 6, 27, 10, 30, 40), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 750, 'climb_rate': -5.0, 'track': 90.0},
            {'expected_state': State.LANDING,  'timestamp': datetime(2020, 6, 27, 10, 30, 50), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 700, 'climb_rate': -5.0, 'track': 90.0},
            {'expected_state': State.LANDING,  'timestamp': datetime(2020, 6, 27, 10, 31,  0), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 650, 'climb_rate': -5.0, 'track': 90.0},
            {'expected_state': State.LANDING,  'timestamp': datetime(2020, 6, 27, 10, 31, 10), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 600, 'climb_rate': 0.0, 'track': 90.0},
            {'expected_state': State.LANDING,  'timestamp': datetime(2020, 6, 27, 10, 31, 20), 'address': 'DD1234', 'ground_speed': 50.0, 'altitude': 600, 'climb_rate': 0.0, 'track': 90.0},
            {'expected_state': State.MOVING,   'timestamp': datetime(2020, 6, 27, 10, 31, 30), 'address': 'DD1234', 'ground_speed': 10.0, 'altitude': 600, 'climb_rate': 0.0, 'track': 90.0},
            {'expected_state': State.GROUND,   'timestamp': datetime(2020, 6, 27, 10, 31, 40), 'address': 'DD1234', 'ground_speed':  0.0, 'altitude': 600, 'climb_rate': 0.0, 'track': 90.0},
            {'expected_state': State.GROUND,  ' timestamp': datetime(2020, 6, 27, 10, 31, 50), 'address': 'DD1234', 'ground_speed':  0.0, 'altitude': 600, 'climb_rate': 0.0, 'track': 90.0},
        ]

        state_machine = StateMachine(elevation=600)

        for message in messages:
            state_machine.add_message(message)

            state = state_machine.get_state(address='DD1234')
            expected_state = message['expected_state']
            self.assertEqual(expected_state, state)

        takeoff_landings = state_machine.takeoff_landings
        self.assertEqual(len(takeoff_landings), 1)
        self.assertEqual(takeoff_landings[0].address, 'DD1234')
        self.assertEqual(takeoff_landings[0].timestamp, datetime(2020, 6, 27, 10, 31, 30))
        self.assertFalse(takeoff_landings[0].is_takeoff)

    def test_aborted_whinch_launch(self):
        """One plane makes a whinch launch which is interrupted."""

        messages = [
            {'expected_state': State.UNKNOWN, ' timestamp': datetime(2020, 6, 27, 10, 30,  0), 'address': 'DD1234', 'ground_speed':  0.0, 'altitude': 600, 'climb_rate':  0.0, 'track': 90.0},
            {'expected_state': State.GROUND,   'timestamp': datetime(2020, 6, 27, 10, 30, 10), 'address': 'DD1234', 'ground_speed':  0.0, 'altitude': 600, 'climb_rate':  0.0, 'track': 90.0},
            {'expected_state': State.MOVING,   'timestamp': datetime(2020, 6, 27, 10, 30, 20), 'address': 'DD1234', 'ground_speed': 10.0, 'altitude': 600, 'climb_rate':  0.0, 'track': 90.0},
            {'expected_state': State.STARTING, 'timestamp': datetime(2020, 6, 27, 10, 30, 30), 'address': 'DD1234', 'ground_speed': 50.0, 'altitude': 600, 'climb_rate':  0.0, 'track': 90.0},
            {'expected_state': State.STARTING, 'timestamp': datetime(2020, 6, 27, 10, 30, 40), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 600, 'climb_rate':  0.0, 'track': 90.0},
            {'expected_state': State.STARTING, 'timestamp': datetime(2020, 6, 27, 10, 30, 50), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 700, 'climb_rate': 10.0, 'track': 90.0},
            {'expected_state': State.STARTING, 'timestamp': datetime(2020, 6, 27, 10, 31,  0), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 650, 'climb_rate': -5.0, 'track': 90.0},
            {'expected_state': State.STARTING, 'timestamp': datetime(2020, 6, 27, 10, 31, 10), 'address': 'DD1234', 'ground_speed': 90.0, 'altitude': 600, 'climb_rate': -5.0, 'track': 90.0},
            {'expected_state': State.STARTING, 'timestamp': datetime(2020, 6, 27, 10, 31, 20), 'address': 'DD1234', 'ground_speed': 50.0, 'altitude': 600, 'climb_rate':  0.0, 'track': 90.0},
            {'expected_state': State.ABORTING_START,   'timestamp': datetime(2020, 6, 27, 10, 31, 30), 'address': 'DD1234', 'ground_speed': 10.0, 'altitude': 600, 'climb_rate':  0.0, 'track': 90.0},
            {'expected_state': State.MOVING,   'timestamp': datetime(2020, 6, 27, 10, 31, 40), 'address': 'DD1234', 'ground_speed': 10.0, 'altitude': 600, 'climb_rate':  0.0, 'track': 90.0},
            {'expected_state': State.GROUND,   'timestamp': datetime(2020, 6, 27, 10, 31, 50), 'address': 'DD1234', 'ground_speed':  0.0, 'altitude': 600, 'climb_rate':  0.0, 'track': 90.0},
        ]

        state_machine = StateMachine(elevation=600)

        for message in messages:
            state_machine.add_message(message)

            state = state_machine.get_state(address='DD1234')
            expected_state = message['expected_state']
            self.assertEqual(expected_state, state)
