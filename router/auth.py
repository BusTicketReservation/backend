import models
import schemas
import utils
import oauth2
import database
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/signupCustomer", response_model=schemas.CustomerOut)
def signupCustomer(customer: schemas.CustomerSignUp, db: Session = Depends(database.get_db),
                   status_code=201):
    if db.query(models.User).filter(models.User.email == customer.email).first():
        raise HTTPException(status_code=400, detail="error")
    
    hashedPassword = utils.hash(customer.password)
    user = models.User(email=customer.email, password=hashedPassword, phone=customer.phone, role="CUSTOMER")
    db.add(user)
    db.commit()
    db.refresh(user)
    customer = models.Customer(name=customer.name, dateOfBirth=customer.dateOfBirth, address=customer.address,
                               userID=user.id,
                               nid = customer.nid )
    db.add(customer)
    db.commit()
    db.refresh(customer)

    customerOut = schemas.CustomerOut(id=customer.id, name=customer.name, dateOfBirth=customer.dateOfBirth,
                                        address=customer.address, email=user.email, phone=user.phone
                                        , nid = customer.nid
                                        )
    return customerOut


@router.post("/signupBus", response_model=schemas.BusOut,
             status_code=201)
def signupBus(bus: schemas.BusSignUp, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.email == bus.email).first():
        raise HTTPException(status_code=400, detail="error")
    
    hashedPassword = utils.hash(bus.password)
    user = models.User(email=bus.email, password=hashedPassword, phone=bus.phone, role="BUS")
    db.add(user)
    db.commit()
    db.refresh(user)
    bus = models.Bus(companyName=bus.companyName, licenseNo=bus.licenseNo, userID=user.id)
    db.add(bus)
    db.commit()
    db.refresh(bus)

    busOut = schemas.BusOut(id=bus.id, companyName=bus.companyName, licenseNo=bus.licenseNo, email=user.email,
                            phone=user.phone)
    return busOut


@router.post("/signin", response_model=schemas.Token, status_code=200)

def signIn(userCredentials: schemas.SignIn, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == userCredentials.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="error")
    if not utils.verify(userCredentials.password, user.password):
        raise HTTPException(status_code=400, detail="error")
    
    accessToken = oauth2.createAccessToken(data={
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "phone": user.phone,
    })

    if user.role == "CUSTOMER":
        customer = db.query(models.Customer).filter(models.Customer.userID == user.id).first()
        tokenData = schemas.Token(
            id=user.id,
            accessToken=accessToken,
            token_type="bearer",
            email=user.email,
            role=user.role,
            name=customer.name
        )
    else:
        bus = db.query(models.Bus).filter(models.Bus.userID == user.id).first()
        tokenData = schemas.Token(
            id=user.id,
            accessToken=accessToken,
            token_type="bearer",
            email=user.email,
            role=user.role,
            name=bus.companyName
        )
    
    return tokenData
