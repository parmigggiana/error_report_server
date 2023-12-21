import os
import time
import uuid
from fastapi import FastAPI, File, UploadFile

files_dir = "received_files"
content_type = "peracotta/error-log"

try:
    os.mkdir(files_dir)
except FileExistsError:
    pass

app = FastAPI()


@app.put("/")
async def put_handler(file: UploadFile = File(...)):
    if file.content_type != content_type:
        return
    contents = await file.read()
    with open(f"{files_dir}/{int(time.time())}_{uuid.uuid4()}", "bw") as fs:
        fs.write(contents)
    # Process the contents of the file here
    return {"filename": file.filename, "contents": contents}
