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

@router.get("/student/profile", response_model=schemas.Student, status_code=200)
def getStudentProfile(db: Session = Depends(database.get_db), currentUser = Depends(oauth2.getCurrentUser)):
    if currentUser.role != "STUDENT"  and db.query(models.Student).filter(models.Student.email != currentUser.email).first():
        raise HTTPException(status_code=400, detail="error")
    student = db.query(models.Student).filter(models.Student.email == currentUser.email).first()
    return student


@router.put("/student/profileUpdate", response_model=schemas.Student, status_code=200)
def updateStudentProfile(updateInfo: schemas.StudentUpdate, db: Session = Depends(database.get_db), currentUser = Depends(oauth2.getCurrentUser)):
    if currentUser.role != "STUDENT"  and db.query(models.Student).filter(models.Student.email != currentUser.email).first():
        raise HTTPException(status_code=400, detail="error")
    student = db.query(models.Student).filter(models.Student.email == currentUser.email).first()
    student.name = updateInfo.name
    student.phone = updateInfo.phone
    student.school = updateInfo.school
    student.college = updateInfo.college
    db.commit()

    db.refresh(student)

    user = db.query(models.User).filter(models.User.email == currentUser.email).first()
    user.name = student.name
    user.phone = student.phone
    db.commit()
    db.refresh(user)

    print(student.name)

    return student