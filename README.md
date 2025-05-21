# Prior Auth Copilot Backend

This is the backend service for the Prior Auth Copilot application, which helps automate medical prior authorization form processing using AI.

## Overview

The backend is built using FastAPI and provides a RESTful API for processing medical prior authorization forms. It uses GPT-4 Vision to extract and process information from uploaded form images or PDFs.

## API Endpoints

### Form Extraction

**Endpoint:** `POST /api/v1/extract-form-data/`

Extracts form data from uploaded medical prior authorization forms using GPT-4 Vision.

#### Request
- **Method:** POST
- **Content-Type:** multipart/form-data
- **Parameters:**
  - `files`: List of files (images/PDFs) [Required]
  - `additional_notes`: Additional context for processing (Optional)

#### Example cURL
```bash
curl -X POST "http://localhost:8000/api/v1/extract-form-data/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@path/to/your/form.pdf" \
  -F "additional_notes=Patient has chronic condition"
```

#### Response
Returns a structured JSON response containing:
- Extracted form data
- Confidence scores for extracted information
- Any processing metadata

## Setup

1. Create a conda environment using the provided environment.yml:
```bash
conda env create -f environment.yml
```

2. Activate the environment:
```bash
conda activate prior-auth-copilot
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python main.py
```

The server will start at `http://localhost:8000`

## Development

The backend follows a modular architecture with:
- FastAPI for the web framework
- Dependency injection for services
- Middleware for CORS support
- Structured error handling
- Type hints and validation

## API Documentation

When the server is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc` 