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
            message = models.Message(sender=senderEmail, receiver=receiverEmail, message=data)
            db.add(message)
            db.commit()
            db.refresh(message)
            await manager.broadcast(data, senderEmail, receiverEmail)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {currentUser.email} left the chat", currentUser.email, teacher_email)