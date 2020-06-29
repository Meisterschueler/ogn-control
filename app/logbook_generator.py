from app.model import LogbookEntry


def create_logbook(takeoff_landings):
    logbook_entries = []

    for event in takeoff_landings:
        if event.is_takeoff:
            logbook_entries.append(LogbookEntry(address=event.address, takeoff_timestamp=event.timestamp))
        else:
            matching_takeoff_entries = [entry for entry in logbook_entries if entry.address == event.address and entry.takeoff_timestamp is not None and entry.takeoff_timestamp < event.timestamp and entry.landing_timestamp is None]
            if len(matching_takeoff_entries) > 0:
                matching_takeoff_entries[0].landing_timestamp = event.timestamp
            else:
                logbook_entries.append(LogbookEntry(address=event.address, landing_timestamp=event.timestamp))

    return logbook_entries
