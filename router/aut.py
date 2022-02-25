import json
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
secretFile = open('config/secret.json', 'r')
file = json.loads(secretFile.read())
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, file["SECRET_KEY"], algorithm=file["ALGORITHM"])
    return encoded_jwt