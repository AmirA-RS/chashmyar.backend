from ast import Str
from re import S
from typing import List
from pydantic import StrBytes
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from Db.Db import Base


class user(Base):
    __tablename__ = "user_info"
    id= Column(Integer, primary_key=True, index=True)
    password = Column(String)
    name = Column(String)
    username = Column(String, unique=True)
    national_number = Column(String, unique=True)
    email = Column(String, unique=True)
    age = Column(Integer)
    eye_grade = Column(String)
    blood_type = Column(String)
    gender = Column(String)
    illness = Column(Boolean)
    avatar = Column(LargeBinary)
    moreInfo = Column(String)
    admin = Column(Boolean)


