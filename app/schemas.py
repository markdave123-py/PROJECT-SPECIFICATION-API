from datetime import datetime
import email

from typing import Optional
from unittest.mock import Base
from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class User(BaseModel):
    user_name: str
    email: EmailStr

class user_email(BaseModel):
    email: EmailStr

class Send(BaseModel):
    admin_email: EmailStr
    body: str
    google_authentication_password: str

class Task_status(BaseModel):
    status: str


class User_response(User):
    
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
     
class participants(BaseModel):
    participant: User_response

    class Config:
        orm_mode = True 




class Create_user_request(BaseModel):
    first_name: str
    last_name:str
    email: EmailStr
    user_name:str
    password: str

class Create_user_response(BaseModel):
    Data: User_response
    Message: str
    
    class Config:
        orm_mode = True

class Token_data(BaseModel):
    id: Optional[str] = None

class Create_project(BaseModel):
    name: str
    description: str

class Get_project(BaseModel):
    name: str
    description: str
    participants: list
    admins: list
    id:int
    project_status: str
    class Config:
        orm_mode = True


class Task_request(BaseModel):
    description: str
    assignedTo: EmailStr
    status: str
    deadline: int

class Task(BaseModel):
    id: int
    description: str
    assignedTo: EmailStr
    status: str
    deadline: str
    class Config:
        orm_mode = True


class Task_create_response(BaseModel):
    Data: Task
    Message: str

    class Config:
        orm_mode = True

class Tasks_response(BaseModel):
    id: int
    description: str
    assignedTo: EmailStr
    status: str

    class Config:
        orm_mode = True


