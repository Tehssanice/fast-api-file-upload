import os
from db import UPLOAD_DIR
from db import engine
from sqlmodel import Session
from typing import Annotated
from fastapi import Header


async def get_session():
    with Session(engine) as session:
        yield session


def save_uploaded_file(file, picturename):
    with open(os.path.join(UPLOAD_DIR, picturename), "wb") as buffer:
        buffer.write(file.file.read())


# Dependency to extract User-Agent header
def get_user_agent(user_agent: Annotated[str | None, Header()] = None):
    return user_agent
