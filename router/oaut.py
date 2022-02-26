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
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(tk, file["SECRET_KEY"], algorithms=[file["ALGORITHM"]])
        information = payload.get("sub")
        result = re.search(pattern, information)
        email, admin = result.group(1), result.group(2)
        if email is None:
            raise credentials_exception
        token_data = token.token_data(email = email, admin = admin)
        return token_data
    except JWTError:
        raise credentials_exception