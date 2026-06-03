import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import generate_batch

app = FastAPI(title="Fiverr Funnel Agent API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


class BatchRequest(BaseModel):
    niche: str
    service: str
    fiverr_url: str
    tone: str = "Professional yet approachable"
    angle: str = ""


@app.get("/")
def health():
    return {"status": "ok", "agent": "fiverr-funnel-agent", "version": "1.0"}


@app.post("/generate-batch")
def generate(req: BatchRequest):
    results = generate_batch(
        niche=req.niche,
        service=req.service,
        fiverr_url=req.fiverr_url,
        tone=req.tone,
        angle=req.angle
    )
    return {"status": "success", "content": results}
