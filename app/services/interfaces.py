from abc import ABC, abstractmethod
from typing import List, Dict, Any
from fastapi import UploadFile
from app.models.response import FormExtractionResponse


class FileHandler(ABC):
    @abstractmethod
    async def validate_file(self, file: UploadFile) -> bool:
        """Validate a single file."""
        pass

    @abstractmethod
    async def process_file(self, file: UploadFile) -> Dict[str, Any]:
        """Process a single file into required format."""
        pass


class AIModelProcessor(ABC):
    @abstractmethod
    async def process_content(
        self, content: List[Dict[str, Any]], additional_context: str = None
    ) -> FormExtractionResponse:
        """Process content using AI model."""
        pass


class ResponseMapper(ABC):
    @abstractmethod
    def map_to_response(self, ai_response: Any) -> FormExtractionResponse:
        """Map AI response to our response model."""
        pass
