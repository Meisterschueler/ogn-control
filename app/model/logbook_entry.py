class LogbookEntry():
    def __init__(self, address, takeoff_timestamp=None, landing_timestamp=None):
        self.address = address
        self.takeoff_timestamp = takeoff_timestamp
        self.landing_timestamp = landing_timestamp

    def __str__(self):
        return "LogbookEntry(address='{address}', takeoff_timestamp='{takeoff_timestamp}', landing_timestamp='{landing_timestamp}')".format(**self.__dict__)
