import datetime
import models
import schemas
import utils
import oauth2
import database
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

manager = utils.connectionManager()

router = APIRouter(
    tags=["Student"],
    prefix="/student"
)


@router.get("/profile", response_model=schemas.Student, status_code=200)
def getStudentProfile(db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)):
    if currentUser.role != "STUDENT" and db.query(models.Student).filter(models.Student.email != currentUser.email).first():
        raise HTTPException(status_code=400, detail="emailError")
    student = db.query(models.Student).filter(
        models.Student.email == currentUser.email).first()
    return student


@router.put("/profileUpdate", response_model=schemas.Student, status_code=200)
def updateStudentProfile(updateInfo: schemas.StudentUpdate, db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)):
    if currentUser.role != "STUDENT" and db.query(models.Student).filter(models.Student.email != currentUser.email).first():
        raise HTTPException(status_code=400, detail="emailError")
    student = db.query(models.Student).filter(
        models.Student.email == currentUser.email).first()
    student.name = updateInfo.name
    student.phone = updateInfo.phone
    student.school = updateInfo.school
    student.college = updateInfo.college
    db.commit()

    db.refresh(student)

    user = db.query(models.User).filter(
        models.User.email == currentUser.email).first()
    user.name = student.name
    user.phone = student.phone
    db.commit()
    db.refresh(user)

    return student


@router.websocket("/ws/{teacher_email}")
async def websocket_endpoint(websocket: WebSocket, teacher_email: str,
                             db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)):

    if currentUser.role != "STUDENT":
        await websocket.close()
        raise HTTPException(status_code=400, detail="error")

    await manager.connect(websocket, teacher_email)
    try:
        while True:
            data = await websocket.receive_text()
            senderEmail = currentUser.email
            receiverEmail = teacher_email
            message = models.Message(
                sender=senderEmail, receiver=receiverEmail, message=data)
            db.add(message)
            db.commit()
            db.refresh(message)
            await manager.broadcast(data, senderEmail, receiverEmail)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {currentUser.email} left the chat", currentUser.email, teacher_email)


@router.post("/buyCourse/{course_id}", status_code=200)
def buyCourse(course_id: int, db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)):
    if currentUser.role != "STUDENT":
        raise HTTPException(status_code=400, detail="roleError")
    if not db.query(models.Student).filter(models.Student.email == currentUser.email).first():
        raise HTTPException(status_code=400, detail="emailError")

    course = db.query(models.Courses).filter(
        models.Courses.id == course_id).first()
    if not course:
        raise HTTPException(status_code=400, detail="courseError")
    courseName = course.name

    courseFee = db.query(models.CourseFees).filter(
        models.CourseFees.courseID == course_id).first()
    
    student = db.query(models.Student).filter(
        models.Student.email == currentUser.email).first()
    
    if db.query(models.CourseEnrollment).filter(models.CourseEnrollment.courseID == course_id, models.CourseEnrollment.studentEmail == currentUser.email).first():
        raise HTTPException(status_code=400, detail="alreadyEnrolled")
    

    if datetime.datetime.now() < courseFee.discountUpTo:
        fees = courseFee.fees - (courseFee.fees * courseFee.discount / 100)
    else:
        fees = courseFee.fees

    enrollment = models.CourseEnrollment(
        courseID=course_id, studentEmail=currentUser.email, studentUserName=currentUser.userName, enrollmentDate=datetime.datetime.now())
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    utils.sendEmail("Welcome to our platform",
                    f"Hello {student.name}, Welcome to our platform. You have successfully enrolled in the {courseName}. Make your payment. Thank you.", student.email)

    
    

    return {
        "courseName": courseName,
        "courseID": course_id,
        "studentName": student.name,
        "studentUserName": student.userName,
        "studentEmail": student.email,
        "fees": fees,
        "enrollmentDate": datetime.datetime.now(),
        "paid": False
    }
