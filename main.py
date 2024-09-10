import datetime
import os
import time
import uuid
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

files_dir = "received_files"

try:
    os.mkdir(files_dir)
except FileExistsError:
    pass

app = FastAPI()


@app.post("/")
async def post_handler(file: UploadFile):
    contents = await file.read()
    with open(f"{files_dir}/{int(time.time())}_{uuid.uuid4()}", "bw") as fs:
        fs.write(contents)
    # Process the contents of the file here
    return {"filename": file.filename, "contents": contents}


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    files = {
        file: {
            "timestamp": datetime.datetime.fromtimestamp(
                int(file.split("_")[0])
            ).strftime("%H:%M - %d %B %Y"),
            "data": None,
        }
        for file in os.listdir(files_dir)
    }
    files[None] = {"timestamp": "", "data": ""}

    return templates.TemplateResponse(
        "index.jinja", {"request": request, "files": files, "name": None}
    )


@app.get("/{name}", response_class=HTMLResponse)
async def get_files(request: Request, name: str = None):
    files = {
        file: {
            "timestamp": datetime.datetime.fromtimestamp(
                int(file.split("_")[0])
            ).strftime("%H:%M - %d %B %Y"),
            "data": open(os.path.join(files_dir, file)).read(),
        }
        for file in os.listdir(files_dir)
    }
    files[None] = {"timestamp": "", "data": ""}
    if name not in files:
        name = None

    return templates.TemplateResponse(
        "index.jinja", {"request": request, "files": files, "name": name}
    )
