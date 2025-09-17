from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime,timedelta
from database import Users,get_db
from sqlalchemy.orm import Session

router=APIRouter(prefix='/auth',tags=['Authentication'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY='bc9dc570c2a6b2d4a72ebcf25bab8ef8'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRES_MINUTES=30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/generate_token/")

def get_hash_pass(password:str):
    return pwd_context.hash(password)

def verify_password(password:str,hashed_password:str):
    return pwd_context.verify(password,hashed_password)

def authenticate_user(username:str,password:str,db:Session=Depends(get_db)):
    user=db.query(Users).filter(Users.email==username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User not found')
    if not verify_password(password,user.hash_pass):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Incorrect password or id')
    return user

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({'exp':expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def verify_access_token(token:str=Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username=payload.get('sub')
        if not username:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User not found')
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User not found')
    
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Not found')
        user=db.query(Users).filter(Users.email==username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Not found.')
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Unexpected Error.')
    
@router.post('/create_new_user/')
def create_user(name:str,email:str,password:str,db:Session=Depends(get_db)):
    temp=db.query(Users).filter(Users.email==email).first()
    if temp:
        raise HTTPException(status_code= status.HTTP_226_IM_USED,detail='E-mail already used')
    hash_pass=get_hash_pass(password)
    new_user=Users(name=name,email=email,hash_pass=hash_pass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/generate_token/')
def generate_token(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid.')
    token=create_access_token(data={"sub":user.email})
    return {"access_token":token,'token_type':'bearer'}