from pydantic import BaseModel, Field

class Stream(BaseModel):
    id: str
    name: str
    source: dict
    media: dict
    site_id: str
    active: bool

class UpdateStreamName(BaseModel):
    name: str

# from pydantic import BaseModel, Field, EmailStr, HttpUrl
# from bson import ObjectId
# from typing import Optional
# from uuid import uuid4, UUID
# from typing import List, Optional
# from pydantic import BaseModel, root_validator

# class Source(BaseModel):
#     host: str
#     port: int
#     path: str
#     protocol: str
#     type: str
#     username: str
#     password: str

# class MediaServer(BaseModel):
#     host: str
#     port: int
#     path: str
#     username: str
#     password: str

# class Media(BaseModel):
#     webrtc: List[MediaServer]
#     rtsp: List[MediaServer]

# class Stream(BaseModel):
#     _id: str
#     name: str
#     source: Source
#     media: Media
#     site_id: str
#     active: bool

# # @root_validator(pre=True)
# # def extract_id(cls, values):
# #         _id = values.get('_id')
# #         if isinstance(_id, ObjectId):
# #             values['id'] = str(_id)
# #         else:
# #             raise ValidationError("Invalid format for '_id'", field_name='id')
# #         return values
# # class Stream(BaseModel):
# #     class Stream(BaseModel):
# #         name: str
# #         source: List["Source"]=[]
# #         media: List["Media"]
# #         site_id: int
# #         active: bool

# #         class Source(BaseModel):
# #             host: str
# #             port: int
# #             path: str
# #             protocol: str
# #             type: str
# #             username: Optional[str]
# #             password: Optional[str]

# #         class Media(BaseModel):
# #             webrtc: List["WebRTC"]
# #             rtsp: List["RTSP"]

# #             class WebRTC(BaseModel):
# #                 host: str
# #                 port: int
# #                 path: str
# #                 username: Optional[str]
# #                 password: Optional[str]

# #             class RTSP(BaseModel):
# #                 host: str
# #                 port: int
# #                 path: str
# #                 username: Optional[str]
# #                 password: Optional[str]

# #     # class Config:
# #     #     allow_population_by_field_name = True
# #     #     arbitrary_types_allowed = True