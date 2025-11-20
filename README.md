# Meme Authenticity Verifier

Uma aplicação para verificar a autenticidade de memes e capturas de tela, utilizando OCR (Tesseract) e IA (Google Gemini) para detectar manipulações e inconsistências.

## Pré-requisitos

Antes de começar, você precisa ter instalado:

1.  **Python 3.10+**: [Baixar Python](https://www.python.org/downloads/)
2.  **Tesseract OCR**: Necessário para extrair texto das imagens.
    - **Windows**: [Baixar Instalador](https://github.com/UB-Mannheim/tesseract/wiki) (Instale em `C:\Program Files\Tesseract-OCR` ou configure o PATH).
    - **Linux**: `sudo apt install tesseract-ocr`
    - **Mac**: `brew install tesseract`

## Instalação e Configuração

Siga estes passos para rodar o projeto localmente após clonar o repositório:

### 1. Criar e Ativar Ambiente Virtual

É recomendado usar um ambiente virtual para não misturar as bibliotecas do projeto com o seu sistema.

**Windows:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar Dependências

O arquivo `requirements.txt` contém apenas as bibliotecas necessárias para o projeto. Execute:

```bash
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

Você precisa de uma chave de API do Google Gemini.

1.  Renomeie o arquivo `.env.example` para `.env`.
2.  Abra o arquivo `.env` e adicione sua chave:
    ```
    GEMINI_API_KEY=sua_chave_aqui
    ```

## Como Rodar

Você precisará de **dois terminais** abertos (ambos com o ambiente virtual ativado).

### Terminal 1: Backend (API)

Inicia o servidor que processa as imagens.

```bash
uvicorn backend.main:app --reload
```

_O backend rodará em: `http://localhost:8000`_

### Terminal 2: Frontend (Interface)

Inicia a interface visual para upload.

```bash
streamlit run frontend_python/app.py
```

_O frontend abrirá automaticamente em: `http://localhost:8501`_

## Estrutura do Projeto

- `backend/`: Código da API FastAPI e serviços (OCR, Gemini).
- `frontend_python/`: Código da interface Streamlit.
- `requirements.txt`: Lista de bibliotecas Python necessárias.
