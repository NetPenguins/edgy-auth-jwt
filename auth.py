'''Authentication driver'''
import os
from datetime import datetime, timedelta # used to handle expiry time for tokens
import jwt # used for encoding and decoding jwt tokens
from fastapi import HTTPException # used to handle error handling
from passlib.context import CryptContext # used for hashing the password
from fastapi.encoders import jsonable_encoder
# from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.User import UserOut, UserIn
    
class Auth():
    '''Auth class used to deal with user authentication'''
    hasher= CryptContext(schemes=['bcrypt'])
    ALGO = 'HS256'
    secret = os.getenv("APP_SECRET_STRING")
    TOKEN_TTL_SECONDS = 0
    TOKEN_TTL_MINUTES = 10
    TOKEN_TTL_HOURS = 0
    TOKEN_TTL_DAYS = 0

    REFRESH_TTL_SECONDS = 0
    REFRESH_TTL_MINUTES = 0
    REFRESH_TTL_HOURS = 12
    REFRESH_TTL_DAYS = 0

    def hash_password(self, password):
        '''Hash the password based on current scheme'''
        return self.hasher.hash(password)

    def verify_password(self, password, encoded_password):
        '''Verify password provided by user'''
        return self.hasher.verify(password, encoded_password)

    def encode_token(self, user: UserOut):
        '''Encode the user token to be delivered and stored for further use.'''
        payload = {
            'exp' : datetime.utcnow() + timedelta(
                days=self.TOKEN_TTL_DAYS,
                hours=self.TOKEN_TTL_HOURS,
                minutes=self.TOKEN_TTL_MINUTES,
                seconds=self.TOKEN_TTL_SECONDS
            ),
            'iat' : datetime.utcnow(),
	        'scope': 'access_token',
            'admin': False,
            'user': jsonable_encoder(user)
        }
        jwt_val = jwt.encode(
            payload,
            self.secret,
            algorithm=self.ALGO
        )

        return jwt_val

    def decode_token(self, token):
        '''Decode the user token'''
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.ALGO])
            if (payload['scope'] == 'access_token'):
                return  True
            raise HTTPException(
                status_code=401,
                headers={'reason': 'Scope for the token is invalid'},
                detail='Scope for the token is invalid'
            )
        except jwt.ExpiredSignatureError as jwt_error:
            raise HTTPException(
                status_code=401,
                headers={'reason': 'Token expirted'},
                detail='Token expired'
            ) from jwt_error
        except jwt.InvalidTokenError as jwt_error:
            raise HTTPException(
                status_code=401, 
                headers={'reason': 'Invalid token'}, 
                detail='Invalid token'
            ) from jwt_error

    def is_user_permitted(self, token, user: UserIn):
        '''Confirm the user is acting on behalf of themselves'''
        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=[self.ALGO]
            )
            token_user = UserOut(**payload.get("user"))
            if user.username == token_user.username:
                return True
            raise HTTPException(
                status_code=401,
                headers={'reason': 'Scope for the token is invalid'},
                detail='Scope for the token is invalid'
            )
        except jwt.ExpiredSignatureError as jwt_error:
            raise HTTPException(
                status_code=401,
                headers={'reason': 'Token expirted'},
                detail='Token expired'
            ) from jwt_error
        except jwt.InvalidTokenError as jwt_error:
            raise HTTPException(
                status_code=401,
                headers={'reason': 'Invalid token'},
                detail='Invalid token'
            ) from jwt_error
    
    def encode_refresh_token(self, username):
        '''Encode the refresh token'''
        payload = {
            'exp' : datetime.utcnow() + timedelta(
                days=self.REFRESH_TTL_DAYS,
                hours=self.REFRESH_TTL_HOURS,
                minutes=self.REFRESH_TTL_MINUTES,
                seconds=self.REFRESH_TTL_SECONDS
            ),
            'iat' : datetime.utcnow(),
	    'scope': 'refresh_token',
            'sub' : username
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm=self.ALGO
        )

    def refresh_token(self, refresh_token):
        '''Create a refresh token'''
        try:
            payload = jwt.decode(refresh_token, self.secret, algorithms=[self.ALGO])
            if (payload['scope'] == 'refresh_token'):
                username = payload['sub']
                new_token = self.encode_token(username)
                new_refresh_token = self.encode_refresh_token(username)
                return {
                    "access_token": new_token,
                    "refresh_token": new_refresh_token
                }
            raise HTTPException(
                status_code=401,
                detail='Invalid scope for token'
            )
        except jwt.ExpiredSignatureError as jwt_error:
            raise HTTPException(
                status_code=401,
                detail='Refresh token expired'
            ) from jwt_error
        except jwt.InvalidTokenError as jwt_error:
            raise HTTPException(
                status_code=401,
                detail='Invalid refresh token'
            ) from jwt_error
    
    
