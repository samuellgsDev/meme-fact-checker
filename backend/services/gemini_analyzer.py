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
    
    # Use gemini-1.5-flash which supports JSON mode
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    Analise esta imagem em busca de sinais de manipulação ou conteúdo enganoso (fake news/memes).
    
    Também realize um OCR visual avançado para extrair TODO o texto visível na imagem, corrigindo erros que o OCR tradicional possa ter cometido.
    
    Texto do OCR Tradicional (para referência): "{extracted_text}"
    
    Responda APENAS com um objeto JSON válido.
    
    Schema do JSON:
    {{
        "is_manipulated": boolean,
        "reasoning": string (Explicação breve em PORTUGUÊS),
        "visual_anomalies": [string] (Lista de anomalias visuais em PORTUGUÊS),
        "text_analysis": string (Análise do conteúdo textual em PORTUGUÊS),
        "verdict": string ("Provavelmente Autêntico", "Suspeito" ou "Provavelmente Manipulado"),
        "extracted_text": string (Todo o texto extraído da imagem, corrigido e formatado)
    }}
    """
    
    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        # Request JSON response explicitly
        response = await model.generate_content_async(
            [prompt, image],
            generation_config={"response_mime_type": "application/json"}
        )
        

        # Parse JSON response
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            # Fallback cleanup if strict JSON mode fails or isn't supported by the lib version
            text_response = response.text.strip()
            if text_response.startswith("```json"):
                text_response = text_response[7:-3]
            elif text_response.startswith("```"):
                text_response = text_response[3:-3]
            data = json.loads(text_response)
        
        return GeminiAnalysis(
            is_manipulated=data.get("is_manipulated", False),
            reasoning=data.get("reasoning", "No reasoning provided"),
            visual_anomalies=data.get("visual_anomalies", []),
            text_analysis=data.get("text_analysis", ""),
            verdict=data.get("verdict", "Unknown"),
            extracted_text=data.get("extracted_text", extracted_text) # Fallback to original OCR if missing
        )
        
    except Exception as e:
        print(f"Gemini Error: {e}")
        return GeminiAnalysis(
            is_manipulated=False,
            reasoning=f"Error during analysis: {str(e)}",
            visual_anomalies=[],
            text_analysis="Error",
            verdict="Error",
            extracted_text=extracted_text
        )
