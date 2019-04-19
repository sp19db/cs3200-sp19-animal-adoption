class Config(object):
    pass


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    pass


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    pass


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
