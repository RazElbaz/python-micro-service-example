import json
# from app.sb_utils.rmq import RmqClient
from app.utils.logger import Logger
# from app.signal_service_client import SignalServiceClient


# from app.schemas.alert import Alert
from app.db import get_client


class StreamsService():

    def __init__(self) -> None:

        self.logger = Logger("streams")
        self.mongo_client = get_client()

    def start(self):
        self.logger.info("Starting streams service")
