from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.get("/fileupload")
async def read_file(file: UploadFile = File(...)):
    return {"file": file.filename}


@app.post("/fileupload")
async def create_file(file: UploadFile):
    return {"file": file.filename}
