from pydantic import BaseModel
from typing import List, Optional

class AnalysisRequest(BaseModel):
    filename: str

class OCRResult(BaseModel):
    text: str
    confidence: float

class GeminiAnalysis(BaseModel):
    is_manipulated: bool
    reasoning: str
    visual_anomalies: List[str]
    text_analysis: str
    verdict: str

class FullAnalysisResponse(BaseModel):
    filename: str
    ocr_result: OCRResult
    gemini_analysis: GeminiAnalysis
