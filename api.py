from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.deep_search import deep_search
import uvicorn
import os

app = FastAPI(title="EchoForge API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    target: str
    target_type: str = "person"
    max_results: int = 20
    deep_search: bool = False
    dark_web: bool = False
    social_media: bool = True

@app.post("/api/search")
async def search(request: SearchRequest):
    try:
        results = await deep_search(
            target=request.target,
            target_type=request.target_type,
            max_results_per_dork=request.max_results,
            deep_search_enabled=request.deep_search,
            dark_web_enabled=request.dark_web,
            social_media_enabled=request.social_media
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
