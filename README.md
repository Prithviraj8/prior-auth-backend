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

### Authentication Request

**Endpoint:** `POST /api/v1/auth-requests/`

Authenticates and processes prior authorization requests.

#### Request
- **Method:** POST
- **Content-Type:** application/json
- **Authorization:** Bearer Token Required
- **Bearer Token:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRucG5hdmZydWJtbHh3c3BjdWVhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Nzc1OTkwNywiZXhwIjoyMDYzMzM1OTA3fQ.RKfHI7e7SnGHXOCAIVJM1FTjfTd0yTip2NTlmpBvJZo`

#### Example cURL
```bash
curl --location 'http://localhost:8000/api/v1/auth-requests/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRucG5hdmZydWJtbHh3c3BjdWVhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Nzc1OTkwNywiZXhwIjoyMDYzMzM1OTA3fQ.RKfHI7e7SnGHXOCAIVJM1FTjfTd0yTip2NTlmpBvJZo' \
--data '{
  "patient_name": "Mary Doe",
  "patient_id": "P123456",
  "procedure_code": "12345",
  "procedure_description": "Knee Arthroscopy",
  "diagnosis_code": "M17.0",
  "diagnosis_description": "Bilateral primary osteoarthritis of knee",
  "medical_justification": "Patient has failed conservative treatment including physical therapy and NSAIDs. Imaging shows significant joint space narrowing",
  "priority": "Standard",
  "payer_name": "Blue Cross Blue Shield",
  "payer_id": "BCBS123",
  "provider_id": "00000000-0000-0000-0000-000000000001"
}'
```

#### Request Body Parameters
- `patient_name`: Full name of the patient
- `patient_id`: Unique identifier for the patient
- `procedure_code`: CPT or HCPCS code for the procedure
- `procedure_description`: Description of the procedure
- `diagnosis_code`: ICD-10 diagnosis code
- `diagnosis_description`: Description of the diagnosis
- `medical_justification`: Clinical rationale for the procedure
- `priority`: Priority level of the request (Standard/Urgent)
- `payer_name`: Name of the insurance payer
- `payer_id`: Unique identifier for the payer
- `provider_id`: UUID of the requesting provider

#### Response
Returns a JSON response containing:
- Authorization status
- Request tracking ID
- Processing details

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