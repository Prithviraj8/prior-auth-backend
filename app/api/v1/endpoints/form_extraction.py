from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
from app.models.response import FormExtractionResponse
from app.services.file_handler import ImageFileHandler
from app.services.gpt_processor import GPTVisionProcessor
from app.services.response_mapper import GPTResponseMapper
from app.services.interfaces import FileHandler, AIModelProcessor, ResponseMapper

router = APIRouter()


async def get_file_handler() -> FileHandler:
    return ImageFileHandler()


async def get_ai_processor() -> AIModelProcessor:
    return GPTVisionProcessor()


async def get_response_mapper() -> ResponseMapper:
    return GPTResponseMapper()


@router.post("/extract-form-data/", response_model=FormExtractionResponse)
async def extract_form_data(
    files: List[UploadFile] = File(...),
    additional_notes: str = None,
    file_handler: FileHandler = Depends(get_file_handler),
    ai_processor: AIModelProcessor = Depends(get_ai_processor),
    response_mapper: ResponseMapper = Depends(get_response_mapper),
):
    """
    Extract form data from uploaded files using GPT-4 Vision.

    - Accepts multiple files (images/PDFs)
    - Optional additional notes for context
    - Returns structured form data with confidence scores
    """
    try:
        # Validate and process files
        processed_contents = []
        for file in files:
            # Validate file
            await file_handler.validate_file(file)

            # Process file
            processed_content = await file_handler.process_file(file)
            if processed_content:
                processed_contents.append(processed_content)

        if not processed_contents:
            raise HTTPException(status_code=400, detail="No valid files to process")

        # Process with AI
        ai_response = await ai_processor.process_content(
            processed_contents, additional_notes
        )

        # Map to response
        return response_mapper.map_to_response(ai_response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")
