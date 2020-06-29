import enum


class State(enum.Enum):
    UNKNOWN, GROUND, MOVING, STARTING, AIRBORNE, LANDING, \
        ABORTING_START, ABORTING_LANDING = range(8)
