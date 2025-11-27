from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.concurrency import run_in_threadpool
from backend.schemas import FullAnalysisResponse, OCRResult, GeminiAnalysis
from backend.utils import resize_image
from backend.services.ocr import extract_text
from backend.services.gemini_analyzer import analyze_image_with_gemini
from dotenv import load_dotenv
import os


load_dotenv()

app = FastAPI(title="Meme Authenticity Verifier")

@app.get("/")
def read_root():
    return {"message": "Meme Authenticity Verifier API is running"}

@app.post("/analyze", response_model=FullAnalysisResponse)
async def analyze_meme(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    contents = await file.read()
    

    resized_contents = await run_in_threadpool(resize_image, contents)
    

    ocr_result = await run_in_threadpool(extract_text, resized_contents)
    

    gemini_result = await analyze_image_with_gemini(resized_contents, ocr_result.text)
    

    if gemini_result.extracted_text:
        ocr_result.text = gemini_result.extracted_text
    
    return FullAnalysisResponse(
        filename=file.filename,
        ocr_result=ocr_result,
        gemini_analysis=gemini_result
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
