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

@router.websocket("/ws/{student_email}")
async def websocket_endpoint(websocket: WebSocket, student_email: str, 
                             db: Session = Depends(database.get_db), currentUser=Depends(oauth2.getCurrentUser)):
    
    if currentUser.role != "TEACHER":
        await websocket.close()
        raise HTTPException(status_code=400, detail="error")
    
    await manager.connect(websocket, student_email)
    try:
        while True:
            data = await websocket.receive_text()
            senderEmail = currentUser.email
            receiverEmail = student_email
            message = models.Message(sender=senderEmail, receiver=receiverEmail, message=data)
            db.add(message)
            db.commit()
            db.refresh(message)
            await manager.send_personal_message(f"{message.sender}: {message.message}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, student_email)
        await manager.broadcast(f"Client {student_email} left the chat")
    