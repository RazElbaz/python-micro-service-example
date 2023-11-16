from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO, WARNING, ERROR, CRITICAL


class Logger():

    def __init__(self, name, level=DEBUG):
        self.logger = getLogger(name)
        self.logger.setLevel(level)
        self.handler = StreamHandler()
        self.handler.setLevel(level)
        self.handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(self.handler)

    def debug(self, msg):
        self.logger.debug(msg)
    
    def info(self, msg):
        self.logger.info(msg)
    
    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)
