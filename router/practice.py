import models
import schemas
import utils
import oauth2
import database
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Practice"]
)

@router.delete("/remove", status_code=200)
def remove(remove: schemas.Remove, db: Session = Depends(database.get_db)):
    student = db.query(models.Student).filter(
        models.Student.email == remove.email).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="error")
    db.delete(student)
    db.commit()
    user = db.query(models.User).filter(
        models.User.email == remove.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="error")
    db.delete(user)
    db.commit()
    
    
    return {"message":"success"}