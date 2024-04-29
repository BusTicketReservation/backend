import datetime
import models
import schemas
import utils
import oauth2
import database
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session


router = APIRouter(
    tags=["AllUsers"],
    prefix="/allUser"
)

@router.get("/blog", status_code= 200)
def get_all_blog(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs
