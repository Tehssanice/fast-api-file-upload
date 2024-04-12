from sqlmodel import SQLModel, Field  # type: ignore
from typing import Annotated
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, LargeBinary
from sqlmodel import SQLModel, Field
from typing import Annotated, Optional

Base = declarative_base()


class Image(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    data: bytes


class UserRegistration(SQLModel):
    name: str
    age: int
    user_image: str


class User(UserRegistration, table=True):
    id: Annotated[int, Field(default=None, primary_key=True)]


class UserProfileIn(BaseModel):
    name: str
    age: int


class UserProfileOut(BaseModel):
    profile: UserProfileIn
    headers: Optional[dict]


# Define the SQLModel for the UserProfile table

class UserProfile(SQLModel, table=True):
    id: Annotated[int, Field(default=None, primary_key=True)]
    # id: int = Field(default=None, primary_key=True)
    username: str
    phone_number: str
    email: str
    profile_picture: str  # This will store the path to the profile picture
