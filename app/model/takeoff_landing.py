class TakeoffLanding():
    def __init__(self, address, timestamp, is_takeoff):
        self.address = address
        self.timestamp = timestamp
        self.is_takeoff = is_takeoff

    def __str__(self):
        return "TakeoffLanding(address='{address}', timestamp='{timestamp}', is_takeoff='{is_takeoff}')".format(**self.__dict__)
