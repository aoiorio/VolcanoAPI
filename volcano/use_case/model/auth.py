from pydantic import BaseModel, Field


class SignUpUserModel(BaseModel):
    email: str = Field(min_length=3)
    password: str = Field(min_length=4)
    confirm_password: str = Field(min_length=4)


class SignInUserModel(BaseModel):
    email: str = Field(min_length=3)
    password: str = Field(min_length=4)
