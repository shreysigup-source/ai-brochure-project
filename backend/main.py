from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from crawler import crawl_website
from extractor import extract_structured_data
from generator import generate_brochure_text

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Brochure Generator API is running!"}


@app.post("/generate-brochure")
def generate_brochure(data: dict):
    url = data.get("url")

    if not url:
        raise HTTPException(status_code=400, detail="Please send a 'url' field in the request body.")

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:
        # Worker 1: crawler.py visits the website and hands back plain text, page by page
        crawled_data = crawl_website(url)

        # Worker 2: extractor.py asks the AI to turn that text into structured JSON
        structured_data = extract_structured_data(crawled_data)

        if structured_data is None:
            raise HTTPException(
                status_code=500,
                detail="Could not understand the content on this website. Please try a different URL."
            )

        # Worker 3: generator.py asks the AI to write the brochure from that JSON
        brochure_text = generate_brochure_text(structured_data)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong while generating the brochure: {e}")

    # main.py puts everything in the response letter and sends it back to the browser
    return {
        "url": url,
        "structured_data": structured_data,
        "brochure": brochure_text
    }