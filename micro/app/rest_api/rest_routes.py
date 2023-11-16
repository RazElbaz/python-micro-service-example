from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
# from app.database import Post
# from app.oauth2 import require_user
# from app.serializers.postSerializers import postEntity, postListEntity
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
from fastapi import Request
from app.schemas.stream import Stream,UpdateStreamName
from app.rest_api import crud
# import logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger('app.routers.post')

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
    Stream.parse_obj(stream).name = stream_data.name
    updated_stream = crud.update_stream(client, stream)
    logger.info(f'Received request to update stream with ID {stream_id}: {stream_data.dict()}')
    return updated_stream