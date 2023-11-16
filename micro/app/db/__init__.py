
from pymongo.mongo_client import MongoClient

from app.config import settings



def get_client():

    client = MongoClient(settings.DATABASE_URL , uuidRepresentation='standard')
    return client
