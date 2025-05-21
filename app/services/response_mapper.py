from typing import Any, Dict
import json
from app.services.interfaces import ResponseMapper
from app.models.response import FormExtractionResponse, FieldData


class GPTResponseMapper(ResponseMapper):
    def map_to_response(
        self, ai_response: FormExtractionResponse
    ) -> FormExtractionResponse:
        """Map GPT response to FormExtractionResponse."""
        # Since we're already getting a FormExtractionResponse, just return it
        return ai_response

    def _map_field_data(self, data: Dict) -> Dict[str, FieldData]:
        """Map dictionary to FieldData objects."""
        return {key: self._create_field_data(value) for key, value in data.items()}

    def _create_field_data(self, data: Dict) -> FieldData:
        """Create FieldData from dictionary."""
        return FieldData(
            value=data.get("value"),
            confidence=data.get("confidence", 0.0),
            is_missing=data.get("is_missing", True),
            source_file=data.get("source_file", ""),
        )
