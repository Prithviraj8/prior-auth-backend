import pytest
from fastapi.testclient import TestClient
from main import app
import io
import json
from PIL import Image
import numpy as np

client = TestClient(app)


@pytest.fixture
def sample_image():
    """Create a sample image for testing."""
    # Create a small black image
    img = Image.fromarray(np.zeros((100, 100), dtype=np.uint8))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)
    return img_byte_arr


def test_successful_form_extraction(sample_image):
    """Test successful form extraction with valid image."""
    files = [("files", ("test_image.png", sample_image, "image/png"))]
    response = client.post(
        "/api/v1/extract-form-data/",
        files=files,
        data={"additional_notes": "Test notes"},
    )

    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "patient_info" in data
    assert "procedure_info" in data
    assert "diagnosis_info" in data
    assert "medical_justification" in data
    assert "insurance_info" in data
    assert "processing_metadata" in data


def test_invalid_file_type():
    """Test error handling for invalid file type."""
    # Create a text file
    text_content = io.StringIO("This is a text file")
    files = [("files", ("test.txt", text_content.getvalue(), "text/plain"))]

    response = client.post("/api/v1/extract-form-data/", files=files)

    assert response.status_code == 400
    assert "file type" in response.json()["detail"].lower()


def test_no_files():
    """Test error handling when no files are provided."""
    response = client.post("/api/v1/extract-form-data/", files=[])

    assert response.status_code == 422  # FastAPI validation error


def test_multiple_files(sample_image):
    """Test handling multiple files."""
    files = [
        ("files", ("test_image1.png", sample_image, "image/png")),
        ("files", ("test_image2.png", sample_image, "image/png")),
    ]

    response = client.post("/api/v1/extract-form-data/", files=files)

    assert response.status_code == 200
    data = response.json()
    assert "processing_metadata" in data
    assert "total_files_processed" in data["processing_metadata"]


def test_large_file():
    """Test error handling for file size limit."""
    # Create a large byte array (11MB)
    large_content = io.BytesIO(b"0" * (11 * 1024 * 1024))

    files = [("files", ("large.png", large_content, "image/png"))]

    response = client.post("/api/v1/extract-form-data/", files=files)

    assert response.status_code == 400
    assert "size" in response.json()["detail"].lower()


def test_field_data_structure(sample_image):
    """Test the structure of field data in response."""
    files = [("files", ("test_image.png", sample_image, "image/png"))]

    response = client.post("/api/v1/extract-form-data/", files=files)

    assert response.status_code == 200
    data = response.json()

    # Check structure of a field
    patient_info = data["patient_info"]
    for field in patient_info.values():
        assert "value" in field
        assert "confidence" in field
        assert "is_missing" in field
        assert "source_file" in field
        assert isinstance(field["confidence"], (int, float))
        assert isinstance(field["is_missing"], bool)
