'''
User Object
'''
from typing import Union
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    '''User Base Model'''
    username: str
    email: EmailStr
    full_name: Union[str, None] = None
    groups: list
    rooms: list

class UserIn(UserBase):
    """
    User model incoming
    """
    password: str

class UserOut(UserBase):
    '''User model outgoing'''
    pass

class UserInDb(UserBase):
    '''User model in database'''
    hashed_password: str
