import models
import schemas
import utils
import oauth2
import database
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Teacher"],
    prefix="/teacher"
)


@router.get("/profile", response_model=schemas.Teacher, status_code=200)
def getTeacherProfile(db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)):
    if currentUser.role != "TEACHER" and db.query(models.Teacher).filter(models.Teacher.email != currentUser.email).first():
        raise HTTPException(status_code=400, detail="emailError")
    teacher = db.query(models.Teacher).filter(
        models.Teacher.email == currentUser.email).first()
    return teacher


@router.put("/profileUpdate", response_model=schemas.Teacher, status_code=200)
def updateTeacherProfile(updateInfo: schemas.TeacherUpdate, db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)):
    if currentUser.role != "TEACHER" and db.query(models.Teacher).filter(models.Teacher.email != currentUser.email).first():
        raise HTTPException(status_code=400, detail="emailError")
    teacher = db.query(models.Teacher).filter(
        models.Teacher.email == currentUser.email).first()
    teacher.name = updateInfo.name
    teacher.phone = updateInfo.phone
    teacher.batch = updateInfo.batch
    teacher.college = updateInfo.college
    teacher.university = updateInfo.university
    teacher.department = updateInfo.department
    teacher.subject = updateInfo.subject
    db.commit()

    db.refresh(teacher)

    user = db.query(models.User).filter(
        models.User.email == currentUser.email).first()
    user.name = teacher.name
    user.phone = teacher.phone
    db.commit()
    db.refresh(user)

    return teacher
