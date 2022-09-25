
from fastapi import APIRouter, Body, Security
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import List
from db.userDb import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user,
    login
)
from models.User import UserIn, UserOut
from auth import Auth

security = HTTPBearer()
auth_handler = Auth()
router = APIRouter()

@router.post(
    "/signup",
    response_description="User data added into the database"
)
async def add_user_data(user: UserIn = Body(...)):
    '''
    ### Signup a new User
    ---
    #### _NOTE:_ If username or email already exist a **409** will be returned
    ---
    '''
    user = jsonable_encoder(user)
    return await add_user(user)

@router.post(
    "/login",
    response_description="User data added into the database"
)
async def login_user(user: UserIn = Body(...)):
    '''
    ### Login existing user
    Upon successful login an `access_token` and `refresh_token` will be returned to the calling entity.
    ```json
    {
        "access_token": "jwt",
        "refresh_token": "jwt"
    }
    ```
    '''
    user = jsonable_encoder(user)
    return await login(user)

@router.get(
    "/",
    response_description="Users retrieved"
)
async def get_users_data() -> List[UserOut]:
    '''Get Users'''
    return await retrieve_users()


@router.get(
    "/{username}",
    response_description="User data retrieved"
)
async def get_user_data(username: str):
    '''Get User'''
    return await retrieve_user(username)

@router.post('/secret')
def secret_data(credentials: HTTPAuthorizationCredentials = Security(security)):
    '''Test Route'''
    token = credentials.credentials
    if(auth_handler.decode_token(token)):
        return 'Top Secret data only authorized users can access this info'

@router.post('/refresh_token')
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    '''Obtain a refresh token for the user'''
    token = credentials.credentials
    get_user_data(id)
    return auth_handler.refresh_token(token)

@router.put("/{username}")
async def update_user_data(
    username: str,
    req: UserIn = Body(...),
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    '''Update User'''
    if auth_handler.is_user_permitted(credentials.credentials, req):
        return await update_user(
            username,
            req
        )
    

@router.delete(
    "/{username}",
    response_description="User data deleted from the database"
)
async def delete_user_data(username: str):
    '''Delete User'''
    return await delete_user(username)
