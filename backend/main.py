from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Brochure Generator API is running!"}

@app.post("/generate-brochure")
def generate_brochure(data: dict):
    url = data["url"]
    return {"message": f"Received URL: {url}"}