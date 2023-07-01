from fastapi import Request, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from docguptea import app
from docguptea.utils import DBConnection
from docguptea.models import UserAuth, GeneralResponse
from docguptea.services.auth import *


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/response_check", tags=["Resource Server"])
def api_response_check():
    response_result = GeneralResponse.get_instance(data={},
                                      status="not_allowed",
                                      message=["Not authenticated"]
                                      )

    try:
        db_msg = ""
        if DBConnection.is_connected():
            db_msg = "Connection Successful to db!"
        else:
            db_msg = "Connection failed to db"

        response_result.message.append(db_msg)

    except Exception as e:
        print("Exception :", e)

    return response_result

@app.post("/auth/signup", summary="Creates new user account", response_model=GeneralResponse, tags=["Auth Server"])
async def signup(response: UserAuth):
    response_result = GeneralResponse.get_instance(data={},
                                      status="not_allowed",
                                      message=["Not authenticated"]
                                      )
    ops_signup(response_result, response)

    return response_result