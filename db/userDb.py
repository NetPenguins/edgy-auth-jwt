'''
User database controller

'''

from os import access
import motor.motor_asyncio
from bson.objectid import ObjectId
from fastapi import HTTPException, Response
from fastapi.security import HTTPBearer
import asyncio
from auth import Auth
from models.User import UserBase, UserOut, UserIn
from os import getenv

MONGO_DETAILS = "mongodb://dev:devapp@mongodb:27017"
MONGO_COLLECTION = "users"

if getenv("MONGO_DETAILS"):
    MONGO_DETAILS = getenv("MONGO_DETAILS")
if getenv("MONGO_COLLECTION"):
    MONGO_DETAILS = getenv("MONGODB_COLLECTION")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
client.get_io_loop = asyncio.get_running_loop
auth_handler = Auth()

security = HTTPBearer

database = client.base

users = database.get_collection(MONGO_COLLECTION)

async def retrieve_users():
    '''Get all users'''
    users_ret = []
    async for user in users.find():
        users_ret.append(UserOut(**user))
    return users_ret


async def add_user(user_data: UserIn) -> UserOut:
    '''Add a user'''
    user_data = UserIn(**user_data)
    username_exists = await users.find_one({"username": user_data.username})
    user_email_exists = await users.find_one({"email": user_data.email})
    
    if username_exists and user_email_exists:
        raise HTTPException(status_code=409, detail='Username and Email already in use')
    elif username_exists:
        raise HTTPException(status_code=409, detail='Username already in use')
    elif user_email_exists:
        raise HTTPException(status_code=409, detail='Email already in use')
    
    hashed_password = auth_handler.hash_password(user_data.password)
    user_data.password = hashed_password
    user = await users.insert_one(user_data.dict())
    new_user = await users.find_one({"_id": user.inserted_id})
    return UserOut(**new_user)

async def retrieve_user(username: str) -> UserOut:
    '''Get a user'''
    user = await users.find_one({"username": username})
    if user:
        return UserOut(**user)

async def login(user_detail: UserIn) -> dict:
    '''Login route'''
    user: UserBase = await users.find_one({"username": user_detail['username']})
    if user is None:
        return HTTPException(status_code=401, detail='Invalid username')
    if not auth_handler.verify_password(user_detail['password'], user['password']):
        return HTTPException(status_code=401, detail='Invalid password')
    access_token = auth_handler.encode_token(UserOut(**user))
    refresh_token = auth_handler.encode_refresh_token(user['username'])
    content = {'status': 'success'}
# {'access_token': access_token, 'refresh_token': refresh_token}
    response = Response()
    response.set_cookie(key='token', value=access_token, httponly=True)
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
    response.status_code = 200
    return response


async def update_user(username: str, data: UserIn):
    '''Update a user'''
    hashed_password = auth_handler.hash_password(data.password)
    data.password = hashed_password
    user: UserBase = await users.find_one({"username": username})
    if user:
        updated_user = await users.update_one(
            {"username": username}, {"$set": data.dict()}
        )
        if updated_user:
            return data
        return False

async def delete_user(username: str):
    '''Delete a user'''
    user = await users.find_one({"username": username})
    if user:
        await users.delete_one({"username": username})
        return True
