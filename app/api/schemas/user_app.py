from pydantic import BaseModel, Field
# from typing import Optional, List
# from datetime import datetime


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str    