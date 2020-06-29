import unittest
from datetime import datetime

from app.model import TakeoffLanding
from app.logbook_generator import create_logbook


class Test(unittest.TestCase):
    def test_simple_flight(self):
        takeoff = TakeoffLanding(address='DD1234', timestamp=datetime(2020, 6, 29, 15, 12, 34), is_takeoff=True)
        landing = TakeoffLanding(address='DD1234', timestamp=datetime(2020, 6, 29, 15, 12, 40), is_takeoff=False)

        logbook = create_logbook([takeoff, landing])

        self.assertEqual(len(logbook), 1)

        entry = logbook[0]
        self.assertEqual(entry.address, takeoff.address)
        self.assertEqual(entry.takeoff_timestamp, takeoff.timestamp)
        self.assertEqual(entry.landing_timestamp, landing.timestamp)

    def test_multiple_flights(self):
        t1 = TakeoffLanding(address='DD0815', timestamp=datetime(2020, 6, 29, 16, 10,  5), is_takeoff=True)
        t2 = TakeoffLanding(address='DD3141', timestamp=datetime(2020, 6, 29, 16, 12, 34), is_takeoff=True)     # Outlanding
        t3 = TakeoffLanding(address='DD4711', timestamp=datetime(2020, 6, 29, 16, 15,  1), is_takeoff=True)

        l1 = TakeoffLanding(address='DD0815', timestamp=datetime(2020, 6, 29, 15, 59, 59), is_takeoff=False)    # Takeoff is missing
        l2 = TakeoffLanding(address='DD3141', timestamp=datetime(2020, 6, 29, 16, 15, 10), is_takeoff=False)
        l3 = TakeoffLanding(address='DD1234', timestamp=datetime(2020, 6, 29, 16, 15, 30), is_takeoff=False)    # From other airport
        l4 = TakeoffLanding(address='DD0815', timestamp=datetime(2020, 6, 29, 16, 20, 34), is_takeoff=False)
        l5 = TakeoffLanding(address='DD0815', timestamp=datetime(2020, 6, 29, 16, 32, 34), is_takeoff=False)    # Here the takeoff is missing again

        logbook = create_logbook(sorted([t1, t2, t3, l1, l2, l3, l4, l5]))

        self.assertEqual(len(logbook), 6)

        e1 = logbook[0]
        self.assertEqual(e1.address, l1.address)
        self.assertIsNone(e1.takeoff_timestamp)
        self.assertEqual(e1.landing_timestamp, l1.timestamp)

        e2 = logbook[1]
        self.assertEqual(e2.address, t1.address)
        self.assertEqual(e2.takeoff_timestamp, t1.timestamp)
        self.assertEqual(e2.landing_timestamp, l4.timestamp)

        e3 = logbook[2]
        self.assertEqual(e3.address, t2.address)
        self.assertEqual(e3.takeoff_timestamp, t2.timestamp)
        self.assertEqual(e3.landing_timestamp, l2.timestamp)

        e4 = logbook[3]
        self.assertEqual(e4.address, t3.address)
        self.assertEqual(e4.takeoff_timestamp, t3.timestamp)
        self.assertIsNone(e4.landing_timestamp)
