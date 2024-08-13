from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from starlette.responses import FileResponse
from services.ai import generate_response

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

async def read_index():
    return FileResponse('static/index.html')

@app.get("/api/gpt")
async def gpt(review: str):
    return generate_response(review)
