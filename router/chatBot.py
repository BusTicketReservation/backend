import ai
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse


router = APIRouter(
    tags=["ChatBot"],
    prefix="/chatBot"
)


@router.get("/", response_model=dict,
            status_code=200)
def getAnswer(question: str):
    response = ai.getAnswer(question)
    return HTMLResponse(response)
