from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from backend.services.detection_service import inspect_url
from backend.services.risk_analysis_service import calculate_risk
from backend.services.response_service import recommend_response

app = FastAPI(title="AI Phishing Detection & Response Agent", description="SOA prototype: Detection, Risk Analysis, and Response services.", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

class AnalyzeRequest(BaseModel):
    url: str = Field(..., min_length=1, max_length=2048)

@app.get("/api/health")
def health():
    return {"status": "ok", "application": "AI Phishing Detection & Response Agent",
            "services": [{"name": "Detection Service", "status": "running"},
                         {"name": "Risk Analysis Service", "status": "running"},
                         {"name": "Response Service", "status": "running"}]}

@app.post("/api/analyze")
def analyze(request: AnalyzeRequest):
    try:
        detection = inspect_url(request.url)
        risk = calculate_risk(detection)
        response = recommend_response(risk)
        return {"url": detection["url"], "prediction": risk["prediction"], "risk_score": risk["risk_score"],
                "risk_level": risk["risk_level"], "reasons": detection["reasons"], "response": response,
                "service_results": {"detection": detection, "risk_analysis": risk, "response": response},
                "note": "Prototype result based on URL rules; it is not a guarantee of safety."}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
