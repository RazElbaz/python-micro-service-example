import pymongo
from app.db import get_client
from app.schemas.stream import Stream ,UpdateStreamName
from pymongo.errors import PyMongoError
from fastapi import HTTPException, status
from typing import List
from app.utils.logger import Logger
from bson import ObjectId


logger = Logger("crud")

def get_streams(client, site_id):
    try:
        db = client["tests"]
        collection = db["streams"]
        query = {"site_id": site_id}
        logger.info(f'Received request for site_id: {query}')
        streams_data = collection.find(query)
        streams = [Stream.parse_obj(stream) for stream in streams_data]
        # logger.info(f'Received request for site_id: {streams}')
        return streams

    except PyMongoError as e:
        # Handle MongoDB errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"MongoDB error: {str(e)}"
        )

    except Exception as e:
        # Handle other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

def get_stream_by_id(client, stream_id):
    db = client["tests"]
    collection = db["streams"]
    try:
        query = {"id": stream_id}
        stream =  collection.find_one(query)
        logger.info(f'Received request for _id: {stream_id}')

        if stream:
            # logger.info(f'stream : {Stream.parse_obj(stream)}')
            # return Stream.parse_obj(stream)
            return stream
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stream not found")

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

#the update of the name with the id field ##works
def update_stream(client, stream):
    db = client["tests"]
    collection = db["streams"]
    logger.info(f'update stream: {stream["name"]}')
    # Assuming stream["id"] is the UUID you want to use for querying
    query = {"id": stream["id"]}

    # Exclude the "id" field from the update to prevent modifying it
    update_data = {key: value for key, value in stream.items() if key != "id"}

    # Update the document based on the query
    result = collection.update_one(query, {"$set": update_data})

    if result.matched_count > 0:
        return {"message": "Stream updated successfully"}
    else:
        return {"message": "Stream not found"}


# #the update of the name with the _id field ##works with request:http://localhost:8000/update_stream/5cf38461-defc-43a5-a7d1-af2e86074a99
# def update_stream(client, stream):
#     db = client["tests"]
#     collection = db["streams"]
#     logger.info(f'update stream: {(stream["_id"])}')
#     query = {"_id": stream["_id"]}

#     # Exclude the "id" field from the update to prevent modifying it
#     update_data = {key: value for key, value in stream.items() if key != "id"}

#     result = collection.update_one(query, {"$set": update_data})

#     if result.matched_count > 0:
#         return {"message": "Stream updated successfully"}
#     else:
#         return {"message": "Stream not found"}

def delete_stream(client, stream_id):
    db = client["tests"]
    collection = db["streams"]
    logger.info(f'delete stream: {stream_id}')

    # Assuming stream_id is the ObjectId you want to use for querying
    query = {"id": stream_id}

    result = collection.delete_one(query)

    if result.deleted_count > 0:
        return {"message": "Stream deleted successfully"}
    else:
        return {"message": "Stream not found"}
    

async def create_streams(client, stream_data):
    db = client["tests"]
    stream = db["streams"]

    new_stream = {
            "id": stream_data.id,
            "name": stream_data.name,
            "source": stream_data.source,
            "media": stream_data.media,
            "site_id": stream_data.site_id,
            "active": stream_data.active,
        }
    
    result = stream.insert_one(new_stream)
    inserted_id = result.inserted_id
    print(f"Inserted stream with _id: {inserted_id}")
    return inserted_id