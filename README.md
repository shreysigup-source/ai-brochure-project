# AI Brochure Generator

An AI-powered web app that turns any company's website into a structured, professional brochure — automatically.

Paste a URL. The app crawls the website, extracts key information using AI, and generates a ready-to-download brochure in seconds.

**Live Demo → [https://ai-brochure-project-1.onrender.com](https://ai-brochure-project-1.onrender.com)**

---

## What It Does

1. You enter a company's website URL
2. The crawler visits the homepage and relevant pages (About, Services, Products, Contact, etc.)
3. An AI model reads the extracted text and structures it into clean, labeled facts (company name, services, industries, contact details)
4. A second AI pass writes a professional brochure from those facts
5. The finished brochure appears on screen, section by section — and can be downloaded as a PDF

---

## Project Structure

```
ai-brochure-project/
│
├── backend/
│   ├── main.py          # FastAPI server — receives URL, calls workers, returns brochure
│   ├── crawler.py       # Visits website pages, extracts plain text
│   ├── extractor.py     # Sends text to AI, gets back structured JSON
│   ├── generator.py     # Sends structured JSON to AI, gets back brochure text
│   ├── requirements.txt # Python dependencies
│   └── .env             # API keys (not pushed to GitHub)
│
└── frontend/
    └── index.html       # Single-file frontend (HTML + CSS + JavaScript)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Plain HTML, CSS, JavaScript (no framework) |
| Backend | Python, FastAPI, Uvicorn |
| Web Crawling | Requests, BeautifulSoup4 |
| AI Model | Llama 3.1 8B (via Groq API) |
| Deployment | Render (backend as Web Service, frontend as Static Site) |

---

## How It Works — The Pipeline

The backend follows a strict manager-worker pattern. `main.py` is the manager — it never does the real work itself. It passes data between three workers, one after another:

```
Browser → main.py → crawler.py → extractor.py → generator.py → main.py → Browser
```

**crawler.py** — Given a URL, visits the homepage and up to 5 additional pages matching keywords like "about", "services", "contact". Returns a dictionary of plain text, one entry per page category.

**extractor.py** — Takes that dictionary, builds a prompt, and asks the AI to return a clean JSON object with fields like `company_name`, `services`, `industries`, and `contact`. This is the "understanding" step.

**generator.py** — Takes that JSON and asks the AI to write a professional brochure with exactly five sections: Overview, Services, Industries, Why Us, and Contact. This is the "writing" step.

The frontend is a single HTML file with three screens — URL input, loading (with live status messages showing which pipeline step is running), and result (brochure rendered as cards, with a Download button that uses the browser's built-in print-to-PDF feature).

---

## Running Locally

**Prerequisites:** Python 3.10+, a free [Groq API key](https://console.groq.com)

**1. Clone the repository**
```bash
git clone https://github.com/your-username/ai-brochure-project.git
cd ai-brochure-project
```

**2. Set up the backend**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

**3. Create a `.env` file inside the `backend` folder**
```
GROQ_API_KEY=your_groq_api_key_here
```

**4. Start the backend server**
```bash
python -m uvicorn main:app --reload
```

**5. Start the frontend server (new terminal)**
```bash
cd frontend
python -m http.server 5500
```

**6. Open in browser**
```
http://localhost:5500
```

---

## Deployment

The project is deployed on [Render](https://render.com) using two separate services:

- **Backend** → Render Web Service (Python/FastAPI)
  - Root Directory: `backend`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
  - Environment Variable: `GROQ_API_KEY`

- **Frontend** → Render Static Site
  - Root Directory: `frontend`
  - Publish Directory: `.`
  - No build command needed

Every `git push` to the `master` branch triggers an automatic redeploy of both services.

> **Note:** The backend runs on Render's free tier, which spins down after 15 minutes of inactivity. The first request after an idle period may take 30–60 seconds to respond while the server wakes up. Subsequent requests are fast.

---

## API Reference

### `GET /`
Health check. Returns:
```json
{"message": "Brochure Generator API is running!"}
```

### `POST /generate-brochure`
Generates a brochure for the given URL.

**Request body:**
```json
{"url": "https://company.com"}
```

**Response:**
```json
{
  "url": "https://company.com",
  "structured_data": {
    "company_name": "...",
    "overview": "...",
    "services": ["..."],
    "products": ["..."],
    "industries": ["..."],
    "differentiators": ["..."],
    "contact": {
      "email": "...",
      "phone": "...",
      "address": "..."
    }
  },
  "brochure": "## Overview\n..."
}
```

---

## Known Limitations

- **Groq free tier rate limit** — The app uses `llama-3.1-8b-instant` via Groq's free tier (32,000 tokens per minute). Very large websites may still occasionally hit this limit.
- **JavaScript-heavy websites** — The crawler uses plain HTTP requests and cannot execute JavaScript. Websites that load their content dynamically (React/Next.js SPAs) may return limited text.
- **Render cold starts** — As mentioned above, the first request after inactivity is slow. This is a free-tier limitation, not a code issue.

---

## What I Learned Building This

- How a full-stack AI pipeline works end to end — from web crawling to structured extraction to text generation
- The manager-worker pattern for keeping backend code organized and each file responsible for exactly one job
- How CORS works and why it exists (the "guard at the door" between frontend and backend)
- The difference between static hosting and server hosting, and why they need separate deployment services
- Real-world constraints of free-tier AI APIs — token limits, rate limits, and how to work within them
- How to deploy a Python FastAPI backend and a plain HTML frontend on Render with automatic deploys on every git push

---

## Author

SHREYSI GUPTA
Built during an AI/ML internship project.