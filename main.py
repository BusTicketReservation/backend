
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware


import models,utils
from database import engine

from router import auth


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)








