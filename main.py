
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware


import models,utils
from database import engine

from router import auth, founder, student
models.Base.metadata.create_all(bind=engine)



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)

app.include_router(founder.router)

app.include_router(student.router)







