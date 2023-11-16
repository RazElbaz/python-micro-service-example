from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.rest_api import rest_routes
from app.config import settings
from app.streams_service  import StreamsService
from app.utils.logger import Logger
# from app.routers import auth, user, post
import uvicorn
from app.db import get_client

app = FastAPI()

logger = Logger("main")


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
# app.include_router(user.router, tags=['Users'], prefix='/api/users')
# app.include_router(post.router, tags=['Posts'], prefix='/api/posts')
app.include_router(rest_routes.router)  # Add the appropriate prefix
# app.include_router(post.router)


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = get_client()


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


@app.get('/health')
def health():
    return {'status': 'ok'}


def get_server():
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - rest_api - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - rest_api - %(levelname)s - %(message)s"
    config = uvicorn.Config("app.__main__:app", 
                            host=settings.HOST ,
                            port=settings.PORT,
                            log_config=log_config,
                            log_level=settings.LOG_LEVEL,
                            reload=False)
    server = uvicorn.Server(config)
    return server  


# server = get_server()
# stream_service = StreamsService()
# stream_service.start()


if __name__ == '__main__':
    print("in")
    server = get_server()
    stream_service = StreamsService()
    stream_service.start()
    server.run()
