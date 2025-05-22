from typing import List, Dict, Any
import openai
from app.core.config import settings
from app.services.interfaces import AIModelProcessor
from app.models.response import FormExtractionResponse, FieldData
import json
import logging

logger = logging.getLogger(__name__)


class GPTVisionProcessor(AIModelProcessor):
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = "gpt-4.1"

    def _create_system_message(self) -> str:
        return """You are an expert medical form analyzer specializing in prior authorization requests. 
        Your task is to extract specific information from medical documents, including handwritten notes, and format it precisely.
        
        IMPORTANT FORMATTING INSTRUCTIONS:
        1. Return ONLY valid JSON matching the exact structure below
        2. For each field:
           - 'value': Extract the actual value (string) or null if not found
           - 'confidence': Score from 0.0 to 1.0 indicating extraction confidence
           - 'is_missing': true if field not found, false if found
           - 'source_file': Filename where the information was found
        3. DO NOT include any explanatory text outside the JSON structure
        4. Ensure all JSON keys exactly match the structure below
        5. For handwritten text, carefully transcribe exactly what is written

        REQUIRED JSON STRUCTURE:
        {
            "patient_info": {
                "name": {"value": "string or null", "confidence": 0.95, "is_missing": false, "source_file": "string"},
                "id": {"value": "string or null", "confidence": 0.95, "is_missing": false, "source_file": "string"}
            },
            "procedure_info": {
                "code": {"value": "string or null", "confidence": 0.95, "is_missing": false, "source_file": "string"},
                "description": {"value": "string or null", "confidence": 0.95, "is_missing": false, "source_file": "string"}
            },
            "diagnosis_info": {
                "primary_diagnosis": {"value": "string or null", "confidence": 0.95, "is_missing": false, "source_file": "string"},
                "symptoms": {"value": "string or null", "confidence": 0.95, "is_missing": false, "source_file": "string"},
                "affected_area": {"value": "string or null", "confidence": 0.95, "is_missing": false, "source_file": "string"}
            },
            "treatment_info": {
                "prescribed_treatment": {"value": "string or null", "confidence": 0.95, "is_missing": false, "source_file": "string"},
                "treatment_type": {"value": "string or null", "confidence": 0.95, "is_missing": false, "source_file": "string"}
            },
            "insurance_info": {
                "provider": {"value": "string or null", "confidence": 0.95, "is_missing": false, "source_file": "string"},
                "policy_number": {"value": "string or null", "confidence": 0.95, "is_missing": false, "source_file": "string"}
            },
            "medical_justification": {"value": "string or null", "confidence": 0.95, "is_missing": false, "source_file": "string"}
        }"""

    async def process_content(
        self, content: List[Dict[str, Any]], additional_context: str = None
    ) -> FormExtractionResponse:
        """Process content using GPT-4 Vision."""
        try:
            # Prepare the message content
            message_content = [
                {
                    "type": "text",
                    "text": self._create_system_message()
                    + "\n\n"
                    + (additional_context if additional_context else ""),
                }
            ]

            # Add images
            for item in content:
                if item["type"] == "image":
                    message_content.append(
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{item['image']}"
                            },
                        }
                    )

            # Call GPT-4 Vision API with exact message structure
            openai_response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": message_content}],
                max_tokens=4000,
                temperature=0.1,
            )

            # Debug log the response
            logger.debug(f"OpenAI API Response: {openai_response}")

            # Extract the response content
            if not hasattr(openai_response, "choices") or not openai_response.choices:
                raise Exception("Invalid response format from OpenAI API")

            response_content = openai_response.choices[0].message.content
            logger.debug(f"Response content: {response_content}")

            # Parse the response content as JSON
            try:
                extracted_data = json.loads(response_content)
                logger.debug(f"Parsed JSON data: {extracted_data}")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse response as JSON: {response_content}")
                raise Exception(f"Failed to parse GPT response as JSON: {str(e)}")

            # Create the response object
            return FormExtractionResponse(
                patient_info=self._map_field_data(
                    extracted_data.get("patient_info", {})
                ),
                procedure_info=self._map_field_data(
                    extracted_data.get("procedure_info", {})
                ),
                diagnosis_info=self._map_field_data(
                    extracted_data.get("diagnosis_info", {})
                ),
                treatment_info=self._map_field_data(
                    extracted_data.get("treatment_info", {})
                ),
                medical_justification=self._create_single_field_data(
                    extracted_data.get("medical_justification", {})
                ),
                insurance_info=self._map_field_data(
                    extracted_data.get("insurance_info", {})
                ),
                processing_metadata={
                    "model": self.model,
                    "total_tokens": (
                        openai_response.usage.total_tokens
                        if hasattr(openai_response, "usage")
                        else 0
                    ),
                    "completion_tokens": (
                        openai_response.usage.completion_tokens
                        if hasattr(openai_response, "usage")
                        else 0
                    ),
                    "prompt_tokens": (
                        openai_response.usage.prompt_tokens
                        if hasattr(openai_response, "usage")
                        else 0
                    ),
                },
            )

        except Exception as e:
            logger.error(f"Error in process_content: {str(e)}")
            raise Exception(f"Error processing with GPT-4 Vision: {str(e)}")

    def _map_field_data(self, data: Dict) -> Dict[str, FieldData]:
        """Map dictionary to FieldData objects."""
        return {
            key: FieldData(
                value=value.get("value"),
                confidence=value.get("confidence", 0.0),
                is_missing=value.get("is_missing", True),
                source_file=value.get("source_file", ""),
            )
            for key, value in data.items()
        }

    def _create_single_field_data(self, data: Dict) -> FieldData:
        """Create a single FieldData object."""
        return FieldData(
            value=data.get("value"),
            confidence=data.get("confidence", 0.0),
            is_missing=data.get("is_missing", True),
            source_file=data.get("source_file", ""),
        )
