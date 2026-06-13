from fastapi import (
    FastAPI,
    UploadFile,
    File
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from pydantic import BaseModel

import os

from services.upload_service import (
    process_pdf
)

from services.chat_service import (
    ask_question
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

class QuestionRequest(
    BaseModel
):
    question: str

@app.get("/")
def root():

    return {
        "status": "running"
    }

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as f:

        f.write(
            await file.read()
        )

    return process_pdf(
        file_path
    )

@app.post("/chat")
def chat(
    request: QuestionRequest
):

    return ask_question(
        request.question
    )