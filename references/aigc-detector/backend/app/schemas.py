from pydantic import BaseModel, Field

class DetectRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=8000)

class DetectResult(BaseModel):
    label: str  # human | ai | uncertain
    score: float
    confidence: str  # high | medium | low
    rationale: str
    detailed_analysis: str
    key_indicators: list[str]
    methodology: str

class DetectResponse(BaseModel):
    result: DetectResult

class DetectRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=8000)

class TraceMark(BaseModel):
    id: str    # 唯一标识符
    start: int  # 开始位置
    end: int    # 结束位置
    type: str   # 标记类型 (如: repetition, perfect_structure, formal_language等)
    reason: str # 标记原因

class MarkTracesResponse(BaseModel):
    original_text: str
    marked_text: str  # 带有HTML标记的文本
    traces: list[TraceMark]  # 具体的标记列表
    explanation: str
