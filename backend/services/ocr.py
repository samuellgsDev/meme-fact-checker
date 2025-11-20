import pytesseract
from PIL import Image
import io
from backend.schemas import OCRResult

import os

# Ensure Tesseract is in your PATH or set it here
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

def extract_text(image_bytes: bytes) -> OCRResult:
    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        # Get detailed data including confidence
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        
        text_parts = []
        confidences = []
        
        for i, text in enumerate(data['text']):
            if text.strip():
                text_parts.append(text)
                # Tesseract returns confidence as 0-100 integer
                try:
                    conf = float(data['conf'][i])
                    if conf != -1:
                        confidences.append(conf)
                except:
                    pass
        
        full_text = " ".join(text_parts)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        return OCRResult(text=full_text, confidence=avg_confidence)
        
    except Exception as e:
        print(f"OCR Error: {e}")
        # Return the error as text so it's visible in the UI
        return OCRResult(text=f"Erro no OCR: {str(e)}", confidence=0.0)
