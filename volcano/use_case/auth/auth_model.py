from pydantic import BaseModel, Field

class SignUpUserModel(BaseModel):
    email: str
    password: str
    confirm_password: str

class SignInUserModel(BaseModel):
    email: str
    password: str