from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Request, UploadFile, File
from pydantic import EmailStr
from sqlalchemy import desc
from sqlalchemy.orm import Session
from router import oaut
import os
from model import user as UserModel
import shutil
from schema import user as UserSchema
from passlib.context import CryptContext
from router import aut
from schema import token
from Db.Db import get_db
from typing import List
import json
from datetime import timedelta
file = json.load(open('config/secret.json', 'rt', encoding='utf8'))
router = APIRouter(tags=['User'], prefix='/user')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post('/signin', response_model=UserSchema.admin_show, summary='User Signin')
def signin(*, db: Session = Depends(get_db), information: UserSchema.user_signin = Body(...), setAdminTrue: bool = Query(False)):
    try:
        password = pwd_context.hash(information.password)
        user = UserModel.user(name=information.name, password=password, email = information.email, admin = setAdminTrue)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except:
        raise HTTPException(status_code=400)


@router.get('/', response_model=List[UserSchema.user_show], summary='All Users Informations')
def getall(*, db: Session = Depends(get_db), get_current_user: token.token_data = Depends(oaut.get_current_user)):
    try:
        if get_current_user.admin:
            users = db.query(UserModel.user).all()
            return users
        else:
            raise HTTPException(status_code=405, detail='not autorized')
    except:
        raise HTTPException(status_code=400)


@router.get('/one', response_model=UserSchema.user_show, summary='One User Informations')
def update(*, db: Session = Depends(get_db), get_current_user: token.token_data = Depends(oaut.get_current_user), id: str = Query(None), national_number: str = Query(None), email: EmailStr = Query(None)):
    try:
        information = ["id", "national_number", "email"]
        if get_current_user.admin:
            for inf in information:
                if locals()[inf] is not None:
                    print(inf)
                    if inf == "id":
                        user = db.query(UserModel.user).filter(
                            UserModel.user.id == locals()[inf]).first()
                    elif inf == "national_number":
                        user = db.query(UserModel.user).filter(
                            UserModel.user.national_number == locals()[inf]).first()
                    elif inf =="email":
                        user = db.query(UserModel.user).filter(
                            UserModel.user.email == locals()[inf]).first()
                    if user is not None:
                        return user
                    else:
                        raise HTTPException(status_code=404, detail='not found')
        else:
            raise HTTPException(status_code=405, detail='not autorized')
    except:
        raise HTTPException(status_code=400)


@router.get('/me', response_model=UserSchema.user_show, summary='Current User Informations')
def update(*, db: Session = Depends(get_db), get_current_user: token.token_data = Depends(oaut.get_current_user)):
    try:
        user = db.query(UserModel.user).filter(
            UserModel.user.email == get_current_user.email).first()
        return user
    except:
        raise HTTPException(status_code=400)


@router.put('/me', response_model=UserSchema.user_show, summary='Current User Update')
def update(*, db: Session = Depends(get_db), get_current_user: token.token_data = Depends(oaut.get_current_user),  information: UserSchema.update= Body(...), avatar: UploadFile = File(''), moreInfo: list = Query(None, description='More Information About User')):
        email = get_current_user.email
        print(email)
        information = {a: b for a, b in information.dict().items() if b is not None}
        if moreInfo:
            moreInfo = json.dumps(moreInfo).encode('utf8')
            db.query(UserModel.user).filter(UserModel.user.email == email).update(
                {'moreInfo': moreInfo}, synchronize_session=False)
        if information:
            db.query(UserModel.user).filter(UserModel.user.email == email).update(
                information, synchronize_session=False)
        user = db.query(UserModel.user).filter(
            UserModel.user.email == email).first()
        if avatar:
            directory = f"D:/chashmyar/avatar_of_users/{user.email}/{user.email}-avatar.png"
            os.mkdir(f"D:/chashmyar/avatar_of_users/{user.email}")
            with open(directory, "wb") as buffer:
                shutil.copyfileobj(avatar.file, buffer)
                db.query(UserModel.user).filter(UserModel.user.email == email).update(
                {'avatar': directory}, synchronize_session=False)
        db.commit()
        return user


@router.delete('/', summary='User Delete')
def delete(*, db: Session = Depends(get_db), get_current_user: token.token_data = Depends(oaut.get_current_user), id: str = Query(None), national_number: str = Query(None), email: EmailStr = Query(None)):
    try:
        if get_current_user.admin:
            information = ["id", "national_number", "email"]
            for inf in information:
                if locals()[inf] is not None:
                    if inf == "id":
                        user = db.query(UserModel.user).filter(
                            UserModel.user.id == locals()[inf]).delete(synchronize_session=False)
                    elif inf == "national_number":
                        user = db.query(UserModel.user).filter(
                            UserModel.user.national_number == locals()[inf]).delete(synchronize_session=False)
                    elif inf =="email":
                        user = db.query(UserModel.user).filter(
                            UserModel.user.email == locals()[inf]).delete(synchronize_session=False)
                    if user:
                        db.commit()
                        return 'user deleted'
                    else:
                        raise HTTPException(status_code=404, detail='not found')
            raise HTTPException(status_code=404, detail='not found')
        else:
            raise HTTPException(status_code=405, detail='not autorized')
    except:
        raise HTTPException(status_code=400)


@router.post('/login', response_model=token.token_show, summary='User Login')
def loggin(db: Session = Depends(get_db), information: oaut.OAuth2PasswordRequestForm = Depends()):
    email = information.username
    password = information.password
    user = db.query(UserModel.user).filter(
        UserModel.user.email == email).first()
    if not user:
        raise HTTPException(detail='not found', status_code=404)
    if not pwd_context.verify(password, user.password):
        raise HTTPException(detail='wrong password', status_code=400)
    access_token_expires = timedelta(
        minutes=file["ACCESS_TOKEN_EXPIRE_MINUTES"])
    access_token = aut.create_access_token(
        data={"sub": f'{user.email}, admincheck:{user.admin}'}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.delete('/logout/all', summary='User Delete Account')
def logout(db: Session = Depends(get_db),  get_current_user: token.token_data = Depends(oaut.get_current_user)):
    try:
        db.query(UserModel.user).filter(UserModel.user.email ==
                                        get_current_user.email).delete(synchronize_session=False)
        db.commit()
        return 'account deleted'
    except:
        raise HTTPException(status_code=400)
