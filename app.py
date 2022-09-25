'''
Title: Endpoints for authentication control
'''
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.responses import JSONResponse
from routes.user import router as UserRouter

description = """
### 🚀 EdgyStack Auth API handles all auth needs.  🔐
## Users 🐑
#### You will be able to:
* **Signup**
* **Login**
* **Get users**
* **Get user**
* **Update User**
* **Delete User**
* **Get Refresh Token**
---
"""

tags_metadata = [
    {
        "name": "User",
        "description": "Operations with users. The **login** logic is also here.",
    }
]

app = FastAPI(
    default_response_class=JSONResponse,
    title="EdgyStack Authentication Server",
    version="0.0.1",
    description=description,
    openapi_tags=tags_metadata,
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    )

app.include_router(UserRouter, tags=["User"], prefix="/user")

@app.get('/')
def health_check():
    """
    Health check endpoint
    """
    return {'status': "good"}
