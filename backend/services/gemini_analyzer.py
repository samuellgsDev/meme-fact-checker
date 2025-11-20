import google.generativeai as genai
import os
from backend.schemas import GeminiAnalysis
import json
from PIL import Image
import io

async def analyze_image_with_gemini(image_bytes: bytes, extracted_text: str) -> GeminiAnalysis:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return GeminiAnalysis(
            is_manipulated=False,
            reasoning="Gemini API Key not found.",
            visual_anomalies=[],
            text_analysis="Error: Missing API Key",
            verdict="Unknown"
        )

    genai.configure(api_key=api_key)
    
    # Use the latest flash model
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    Analise esta imagem em busca de sinais de manipulação ou conteúdo enganoso (fake news/memes).
    
    Texto Extraído (OCR): "{extracted_text}"
    
    Por favor, forneça uma resposta em JSON com os seguintes campos:
    - is_manipulated (boolean): true se houver fortes sinais de manipulação.
    - reasoning (string): Uma breve explicação do porquê (EM PORTUGUÊS).
    - visual_anomalies (list of strings): Quaisquer artefatos visuais como fontes incompatíveis, pixelização ao redor do texto, photoshop ruim (EM PORTUGUÊS).
    - text_analysis (string): Análise do conteúdo textual. É inflamatório? Combina com o contexto visual? (EM PORTUGUÊS).
    - verdict (string): "Provavelmente Autêntico", "Suspeito" ou "Provavelmente Manipulado".
    
    Retorne APENAS JSON válido.
    """
    
    try:
        image = Image.open(io.BytesIO(image_bytes))
        # Use async generation to avoid blocking
        response = await model.generate_content_async([prompt, image])
        
        # Simple cleanup to ensure we get JSON
        text_response = response.text.strip()
        if text_response.startswith("```json"):
            text_response = text_response[7:-3]
        
        data = json.loads(text_response)
        
        return GeminiAnalysis(
            is_manipulated=data.get("is_manipulated", False),
            reasoning=data.get("reasoning", "No reasoning provided"),
            visual_anomalies=data.get("visual_anomalies", []),
            text_analysis=data.get("text_analysis", ""),
            verdict=data.get("verdict", "Unknown")
        )
        
    except Exception as e:
        print(f"Gemini Error: {e}")
        return GeminiAnalysis(
            is_manipulated=False,
            reasoning=f"Error during analysis: {str(e)}",
            visual_anomalies=[],
            text_analysis="Error",
            verdict="Error"
        )
