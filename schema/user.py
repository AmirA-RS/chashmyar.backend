from enum import Enum
from tkinter import N
from tkinter.messagebox import NO
from pydantic import BaseModel, EmailStr, Field
from typing import Union
import json


class user_signin(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)


class user_show(BaseModel):
    name: str = Field(...)
    national_number: str = Field(None, max_length=10, min_length=10, description='without dash or hyphen')
    email : EmailStr = Field(None)
    age: int = Field(None, min=1)
    eye_grade: str = Field(None)
    blood_type: str = Field(None)#Enum[None, 'A+', 'B+', 'AB+', 'O+', 'A-', 'B-', 'AB-', 'O-']
    gender: str = Field(None)#Enum[None, 'male', 'female']
    illness: bool = Field(None, description='experience of eye illness')
    moreInfo: str = Field(None)
    avatar: str = Field(None)
    admin: bool = Field(None)
    class Config():
        orm_mode = True

class admin_show(user_show):
    class Config():
        orm_mode = True

        
class update(BaseModel):
    name: str = Field(None)
    password: str = Field(None)
    national_number: str = Field(None, max_length=10, min_length=10, description='without dash or hyphen')
    email : EmailStr = Field(None)
    age: int = Field(None, min=1)
    eye_grade: str = Field(None)
    blood_type: str = Field(None)#Enum[None, 'A+', 'B+', 'AB+', 'O+', 'A-', 'B-', 'AB-', 'O-']
    gender: str = Field(None)#Enum[None, 'male', 'female']
    illness: bool = Field(None, description='experience of eye illness')
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    #moreinfo: list = Field([])

