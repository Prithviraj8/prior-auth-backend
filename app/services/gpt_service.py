from fastapi import UploadFile
from typing import List, Dict
import base64
import openai
from app.core.config import settings
from app.models.response import FormExtractionResponse, FieldData

openai.api_key = settings.OPENAI_API_KEY


async def encode_image_to_base64(file: UploadFile) -> str:
    """Convert image file to base64 string."""
    contents = await file.read()
    await file.seek(0)  # Reset file pointer
    return base64.b64encode(contents).decode("utf-8")


async def process_files_with_gpt(
    files: List[UploadFile], additional_notes: str = None
) -> FormExtractionResponse:
    """Process files with GPT-4 Vision and extract form data."""

    # Prepare images for GPT-4 Vision
    images = []
    for file in files:
        if file.content_type.startswith("image/"):
            base64_image = await encode_image_to_base64(file)
            images.append(
                {"type": "image", "image": base64_image, "source": file.filename}
            )

    # Prepare the system message
    system_message = """You are an expert medical form analyzer. Extract information from the provided medical documents 
    and organize it according to the prior authorization form fields. For each field:
    - Extract the value if found
    - Provide a confidence score (0-1)
    - Indicate if the field is missing
    - Note which file the information came from"""

    # Prepare the user message
    user_message = "Please analyze these medical documents and extract information for a prior authorization form."
    if additional_notes:
        user_message += f"\nAdditional context: {additional_notes}"

    try:
        # Call GPT-4 Vision API
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": system_message},
                {
                    "role": "user",
                    "content": [{"type": "text", "text": user_message}, *images],
                },
            ],
            max_tokens=4000,
        )

        # Process GPT's response and structure it
        # This is a simplified example - you'll need to parse GPT's response
        # and map it to your form fields

        return FormExtractionResponse(
            patient_info={
                "name": FieldData(
                    value="John Doe",  # Replace with actual extracted value
                    confidence=0.95,
                    is_missing=False,
                    source_file="document1.jpg",
                ),
                # Add other patient info fields
            },
            procedure_info={
                # Add procedure fields
            },
            diagnosis_info={
                # Add diagnosis fields
            },
            medical_justification=FieldData(
                value="Sample justification",  # Replace with actual extracted value
                confidence=0.8,
                is_missing=False,
                source_file="document1.jpg",
            ),
            insurance_info={
                # Add insurance fields
            },
            processing_metadata={
                "total_files_processed": str(len(files)),
                "gpt_model": "gpt-4-vision-preview",
            },
        )

    except Exception as e:
        raise Exception(f"Error calling GPT-4 Vision API: {str(e)}")
