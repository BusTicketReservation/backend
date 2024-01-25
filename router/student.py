import models
import schemas
import utils
import oauth2
import database
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Student"]
)

@router.get("/student/profile", response_model=schemas.Student)
def getStudentProfile(db: Session = Depends(database.get_db), currentUser = Depends(oauth2.getCurrentUser)):
    if currentUser.role != "STUDENT"  and db.query(models.Student).filter(models.Student.email != currentUser.email).first():
        raise HTTPException(status_code=400, detail="error")
    student = db.query(models.Student).filter(models.Student.email == currentUser.email).first()
    return student