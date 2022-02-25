from pickletools import pyfloat, pylong
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
import json
from schema import token
import re

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")
secretFile = open('config/secret.json', 'r')
file = json.loads(secretFile.read())
pattern = re.compile(r'^(.+), admincheck:(.+)$')

def get_current_user(tk: str = Depends(oauth2_scheme)):
    print(1)
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print(1)
        payload = jwt.decode(tk, file["SECRET_KEY"], algorithms=[file["ALGORITHM"]])
        print(payload)
        information = payload.get("sub")
        result = re.search(pattern, information)
        print(result)
        username, admin = result.group(1), result.group(2)
        print('........................')
        print(admin)
        if username is None:
            raise credentials_exception
        token_data = token.token_data(username = username, admin = admin)
        print(1)
        return token_data
    except JWTError:
        raise credentials_exception

def autorize_user(tk: str = Depends(oauth2_scheme)):
    print('salam')
    payload = jwt.decode(tk, file["SECRET_KEY"], algorithms=[file["ALGORITHM"]])
    result = payload.get("sub")
    result = re.search(pattern, result)
    username, admin = result.group(1), result.group(2)
    print(".......................................")
    print(admin)
    if admin == "None":
        admin = False
    if admin:
        return 1
    else:
        return 0