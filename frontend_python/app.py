import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="Verificador de Memes", layout="wide")

st.title("🕵️‍♂️ Verificador de Autenticidade de Memes e Prints")
st.markdown("Envie uma imagem para verificar se há manipulação usando OCR e Inteligência Artificial.")

uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(uploaded_file, caption="Imagem Enviada", use_container_width=True)
        
    with col2:
        if st.button("Analisar Imagem"):
            with st.spinner("Analisando..."):
                try:
                    # Prepare file for API
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post("http://localhost:8000/analyze", files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Display Verdict
                        verdict = data['gemini_analysis']['verdict']
                        # Adjust logic for Portuguese verdicts
                        color = "green" if "Autêntico" in verdict else "red" if "Manipulado" in verdict else "orange"
                        st.markdown(f"### Veredito: :{color}[{verdict}]")
                        
                        # Display OCR Data
                        with st.expander("📝 Extração OCR (Análise de Texto)"):
                            st.write(f"**Texto Extraído:** {data['ocr_result']['text']}")
                        
                        # Display AI Analysis
                        with st.expander("🤖 Análise de IA (Gemini)"):
                            st.write(f"**Raciocínio:** {data['gemini_analysis']['reasoning']}")
                            
                            st.markdown("**Anomalias Visuais:**")
                            for anomaly in data['gemini_analysis']['visual_anomalies']:
                                st.markdown(f"- {anomaly}")
                                
                            st.markdown("**Análise Textual:**")
                            st.write(data['gemini_analysis']['text_analysis'])
                            
                    else:
                        st.error(f"Erro: {response.status_code} - {response.text}")
                        
                except Exception as e:
                    st.error(f"Erro de Conexão: {e}. Certifique-se de que o backend está rodando na porta 8000.")

st.markdown("---")
st.markdown("Construído com FastAPI, Tesseract e Google Gemini.")
