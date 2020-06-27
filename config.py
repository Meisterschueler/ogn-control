import os

class BaseConfig:
    SECRET_KEY = "i-like-ogn"


class ProductionConfig(BaseConfig):
    ELEVATION = 0.0 # Set this to the elevation of your airfield


class DevelopmentConfig(BaseConfig):
    ELEVATION = 602.0   # The logfile for development was recorded at Königsdorf (elev: 602m)


configs = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': DevelopmentConfig
}
