from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from process import processor  # Assuming process.py is in the same directory or adjust import path

app = FastAPI()

# Enable CORS to allow React frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React runs on port 3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to format search results as JSON (replacing create_url_blocks)
def format_sources(urls):
    sources = []
    for url_group in urls:
        for u in url_group:
            sources.append({"url": u.get("url"), "title": u.get("title")})
    return sources

@app.post("/process")
async def process_text(text: str = Form(...)):
    # Call the processor function from process.py
    markdown_result, searches = processor(text)
    # Format searches as JSON instead of HTML
    sources = format_sources(searches)
    return {"result": markdown_result, "sources": sources}

# Run with: uvicorn app:app --reload