import axios from "axios";

// This is where main.py (FastAPI/uvicorn) is running locally.
// If your backend ever runs on a different port, update it here.
const API_BASE_URL = "http://127.0.0.1:8000";

/**
 * Sends the company URL to the backend and waits for the finished brochure.
 * The backend internally calls crawler.py -> extractor.py -> generator.py
 * and returns { url, structured_data, brochure }.
 */
export async function generateBrochure(url) {
  const response = await axios.post(`${API_BASE_URL}/generate-brochure`, { url });
  return response.data;
}