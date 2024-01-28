import models
import schemas
import utils
import oauth2
import database
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session


router = APIRouter(
    tags=["Founder"]
)


@router.post("/registerTeacher", response_model=schemas.Teacher, status_code=201)
def registerTeachers(teacher: schemas.TeacherSignup, db: Session = Depends(database.get_db),
                     currentUser=Depends(oauth2.getCurrentUser)):
    if currentUser.role != "FOUNDER":
        raise HTTPException(status_code=400, detail="error")
    if db.query(models.User).filter(models.User.email == teacher.email).first():
        raise HTTPException(status_code=400, detail="error")
    user = models.User(email=teacher.email, phone=teacher.phone, name=teacher.name,
                       password=utils.hash(teacher.password), role="TEACHER")
    db.add(user)
    db.commit()
    db.refresh(user)

    teacher = models.Teacher(email=teacher.email, phone=teacher.phone, name=teacher.name,
                             batch=teacher.batch, college=teacher.college, university=teacher.university,
                             department=teacher.department, subject=teacher.subject)
    db.add(teacher)
    db.commit()
    db.refresh(teacher)

    return teacher
