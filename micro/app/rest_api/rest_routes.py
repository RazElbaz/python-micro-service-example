from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from uuid import uuid4
# from app.database import Post
# from app.oauth2 import require_user
# from app.serializers.postSerializers import postEntity, postListEntity
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
from fastapi import Request
from app.schemas.stream import Stream,UpdateStreamName,CreateStream
from app.rest_api import crud
# import logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger('app.routers.post')
import uuid
from app.utils.logger import Logger

logger = Logger("rest_routes")
router = APIRouter()

@router.get('/{site_id}')
def get_streams(request: Request,site_id):
    client = request.app.mongodb_client
    streams = crud.get_streams(client, site_id)
    logger.info(f'Received request for site_id: {site_id}')
    return streams

@router.put('/update_stream/{stream_id}')
async def update_stream(request: Request, stream_id: str, stream_data: UpdateStreamName):
    client = request.app.mongodb_client
    stream = crud.get_stream_by_id(client, stream_id)
    logger.debug(f"updating stream  {stream}")
    stream["name"] = stream_data.name
    updated_stream = crud.update_stream(client, stream)
    logger.info(f'Received request to update stream with ID {stream_id}: {stream_data.dict()}')
    return updated_stream

@router.delete('/{stream_id}')
async def update_stream(request: Request, stream_id: str):
    client = request.app.mongodb_client
    logger.debug(f'deleting stream: {stream_id}')
    result  = crud.delete_stream(client, stream_id)
    return result 


@router.post('/create_stream')
async def create_stream(request: Request, stream_data: CreateStream):
    try:
        client = request.app.mongodb_client

        new_stream_id = await crud.create_streams(client, stream_data) #the function returns a string of the id
     
        # new_stream = get_stream_by_id(client, new_stream_id)
        # logger.info(f'Received request to create stream with ID {new_stream_id}: {stream_data.dict()}')
        # logger.info(new_stream)
        # return new_stream

        logger.info(f'Received request to create stream with ID {new_stream_id}: {stream_data.dict()}')
        return {"message": "Stream created successfully"}


    except Exception as e:
        logger.error(f"Error creating stream: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_stream_by_id(client, stream_id):
    db = client["tests"]
    collection = db["streams"]
    query = {"_id": ObjectId(stream_id)}
    stream = collection.find_one(query)
    
    if stream:
        return Stream(**stream)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stream not found")
