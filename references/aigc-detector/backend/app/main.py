from fastapi import FastAPI, HTTPException
from app.schemas import DetectRequest, DetectResponse, DetectResult, MarkTracesResponse
from app.detector import detect, mark_ai_traces

app = FastAPI(title="AI Detector")

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/detect", response_model=DetectResponse)
def detect_api(req: DetectRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text is empty")
    result = detect(req.text)
    return DetectResponse(result=DetectResult(**result))

@app.post("/api/mark-traces", response_model=MarkTracesResponse)
def mark_traces_api(req: DetectRequest):  # 使用DetectRequest
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text is empty")
    result = mark_ai_traces(req.text)
    return MarkTracesResponse(**result)
