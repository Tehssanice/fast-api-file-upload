from models import UserProfileIn, UserProfileOut
from fastapi import HTTPException
import os
from fastapi import APIRouter, UploadFile, File, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from models import Image, UserRegistration, UserProfile
from deps import save_uploaded_file, get_user_agent,  get_session
from db import UPLOAD_DIR
from fastapi.responses import JSONResponse
import shutil

router = APIRouter()


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...), session: Session = Depends(get_session)):
    # Ensure the upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save the uploaded file to the upload directory
    with open(os.path.join(UPLOAD_DIR, file.filename), "wb") as buffer:
        buffer.write(file.file.read())

    # Save the image details to the database
    image_data = file.file.read()
    image = Image(name=file.filename, data=image_data)
    session.add(image)
    session.commit()

    return {"filename": file.filename}


@router.get("/image/{filename}")
async def get_image(filename: str):
    # Check if the file exists
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    # Read the file content
    with open(file_path, "rb") as file:
        content = file.read()

    return content


@router.post("/register-user")
async def register_user(user: UserRegistration, file: UploadFile = File(...), request_header: str = Header(None)):
    save_uploaded_file(file, user.user_image)
    response_headers = {"Response-Header": request_header}
    return {"message": "User registered", "headers": response_headers}


# @router.post("/profiles/")
# async def create_profile(name: str, age: int,  user_image: UploadFile = File(...), session: Session = Depends(get_session), user_agent: str = Depends(get_user_agent)):
#     try:
#         # Save profile picture to disk
#         file_location = f"profile_pictures/{user_image.filename}"
#         with open(file_location, "wb") as buffer:
#             shutil.copyfileobj(user_image.file, buffer)

#         # Create a new user profile record
#         user_profile = UserRegistration(
#             name=name, age=age, user_image=file_location)
#         session.add(user_profile)
#         session.commit()
#         session.refresh(user_profile)
#         print(user_profile)

#         # Convert UserProfile to dictionary to make it a JSON-serializable format before returning it

#         return JSONResponse(content={"profile": user_profile.dict(), "headers": {"user_agent": user_agent}})
#     except Exception as e:
#         return JSONResponse(status_code=400, content={"message": str(e)})
#         # raise HTTPException(status_code=500, detail="Internal Server Error")


# @router.get("/profilessss/{profile_id}")
# def get_profile(profile_id: int, session: Session = Depends(get_session), user_agent: str = Depends(get_user_agent)):
#     profile = session.get(UserRegistration, profile_id)
#     if profile is None:
#         raise HTTPException(status_code=404, detail="Profile not found")

#     # Return the profile and headers
#     return JSONResponse(content={"profile": profile.dict(), "headers": {"user_agent": user_agent}})


# @router.post("/profilesss/")
# async def create_profile(
#     profile: UserProfileIn,
#     user_image: UploadFile = File(...),
#     session: Session = Depends(get_session),
#     user_agent: str = Depends(get_user_agent)
# ):
#     try:
#         # Validate input parameters
#         if not profile.name:
#             raise HTTPException(status_code=400, detail="Name cannot be empty")
#         if profile.age <= 0:
#             raise HTTPException(
#                 status_code=400, detail="Age must be a positive integer")

#         # Save profile picture to disk
#         file_location = f"profile_pictures/{user_image.filename}"
#         with open(file_location, "wb") as buffer:
#             shutil.copyfileobj(user_image.file, buffer)

#         # Create a new user profile record
#         user_profile = UserRegistration(
#             name=profile.name, age=profile.age, user_image=file_location)
#         session.add(user_profile)
#         session.commit()
#         session.refresh(user_profile)

#         # Return the created profile
#         return UserProfileOut(
#             profile=user_profile,
#             headers={"user_agent": user_agent}
#         )
#     except FileNotFoundError:
#         raise HTTPException(status_code=400, detail="Invalid file")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# Route to create a user profile
@router.post("/profiles/")
async def create_profile(user: UserProfile, profile_picture: UploadFile = File(...), session: Session = Depends(get_session), user_agent: str = Depends(get_user_agent)):
    try:
        # Save profile picture to disk
        file_location = f"profile_pictures/{profile_picture.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(profile_picture.file, buffer)

        # Create a new user profile record
        user_profile = UserProfile(
            username=user.username, phone_number=user.phone_number, email=user.email, profile_picture=file_location)
        session.add(user_profile)
        session.commit()
        session.refresh(user_profile)
        print(user_profile)

        # Convert UserProfile to dictionary to make it a JSON-serializable format before returning it

        return JSONResponse(content={"profile": user_profile.dict(), "headers": {"user_agent": user_agent}})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
        # raise HTTPException(status_code=500, detail="Internal Server Error")

# Route to get a profile by ID


@router.get("/profiles/{profile_id}")
def get_profile(profile_id: int, session: Session = Depends(get_session), user_agent: str = Depends(get_user_agent)):
    profile = session.get(UserProfile, profile_id)
