from fastapi import FastAPI, UploadFile, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Annotated
from deps import get_session


app = FastAPI()


class UserCreate(SQLModel):
    name: str
    age: int
    is_married: bool
    file: str


class User(UserCreate, table=True):
    id: int | None = Field(default=None, primary_key=True)


sqlite_file_name = "userbase.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)


@app.post("/fileupload")
async def create_file(file: UploadFile):
    return {"file": file.filename}


@app.post("/user/")
async def create_user(user: UserCreate, session: Annotated[Session, Depends(get_session)]):
    with Session(engine) as session:
        user_1 = User(name=user.name, age=user.age,
                      is_married=user.is_married, gender=user.gender)
        session.add(user_1)
        session.commit()

    return {"name": user.name, "age": user.age, "is_married": user.is_married, "gender": user.gender}
