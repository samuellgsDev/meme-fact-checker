import pytesseract
from PIL import Image
import io
from backend.schemas import OCRResult

import os


tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

def extract_text(image_bytes: bytes) -> OCRResult:
    try:
        image = Image.open(io.BytesIO(image_bytes))
        

        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        
        text_parts = []
        confidences = []
        
        for i, text in enumerate(data['text']):
            if text.strip():
                text_parts.append(text)

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

        return OCRResult(text=f"Erro no OCR: {str(e)}", confidence=0.0)
