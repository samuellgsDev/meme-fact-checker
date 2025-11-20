# Meme Authenticity Verifier - Setup & Run

## Prerequisites

1.  **Python 3.10+**
2.  **Tesseract OCR** installed on your system.
    - Windows: [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki)
    - Ensure `tesseract.exe` is in your PATH or update `backend/services/ocr.py`.

## Setup

1.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    - Rename `.env.example` to `.env`.
    - Add your Google Gemini API Key:
      ```
      GEMINI_API_KEY=your_actual_key_here
      ```

## Running the Application

You need to run the backend and frontend in separate terminals.

### Terminal 1: Backend (FastAPI)

```bash
uvicorn backend.main:app --reload
```

_The API will be available at `http://localhost:8000`_

### Terminal 2: Frontend (Streamlit)

```bash
streamlit run frontend_python/app.py
```

_The UI will open in your browser at `http://localhost:8501`_
