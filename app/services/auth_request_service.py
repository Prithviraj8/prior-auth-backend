from datetime import datetime
from typing import List, Optional
from uuid import UUID
import logging

from ..models.auth_request import AuthRequestCreate, AuthRequestResponse
from ..database.session import supabase

logger = logging.getLogger(__name__)

# Fixed UUID for service role user
SERVICE_ROLE_USER_ID = "00000000-0000-0000-0000-000000000001"

class AuthRequestService:
    def create_auth_request(self, request: AuthRequestCreate, user: dict) -> AuthRequestResponse:
        logger.debug(f"Creating auth request for user: {user}")
        
        # Get the user ID based on the type of user
        if user.get("role") == "service_role":
            current_user_id = SERVICE_ROLE_USER_ID
            logger.debug("Using service role ID")
        else:
            current_user_id = user["id"]
            logger.debug(f"Using user ID: {current_user_id}")

        # Prepare data for insertion
        auth_request_data = {
            "patient_name": request.patient_name,
            "patient_id": request.patient_id,
            "procedure_code": request.procedure_code,
            "procedure_description": request.procedure_description,
            "diagnosis_code": request.diagnosis_code,
            "diagnosis_description": request.diagnosis_description,
            "medical_justification": request.medical_justification,
            "priority": request.priority,
            "payer_name": request.payer_name,
            "payer_id": request.payer_id,
            "status": "PENDING",
            "provider_id": current_user_id,
            "submitted_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        try:
            logger.debug(f"Attempting to insert auth request with data: {auth_request_data}")
            # Insert into Supabase with RLS enabled
            response = (
                supabase.table("auth_requests")
                .insert(auth_request_data)
                .execute()
            )
            
            logger.debug(f"Supabase response: {response}")
            
            if not response.data:
                raise Exception(f"No data returned from Supabase. Response: {response}")

            # Get the created record
            created_record = response.data[0]
            logger.debug(f"Created record: {created_record}")

            # Convert to response model
            return AuthRequestResponse(
                id=UUID(created_record["id"]),
                patient_name=created_record["patient_name"],
                patient_id=created_record["patient_id"],
                procedure_code=created_record["procedure_code"],
                procedure_description=created_record["procedure_description"],
                diagnosis_code=created_record["diagnosis_code"],
                diagnosis_description=created_record["diagnosis_description"],
                medical_justification=created_record["medical_justification"],
                priority=created_record["priority"],
                payer_name=created_record.get("payer_name"),
                payer_id=created_record.get("payer_id"),
                status=created_record["status"],
                submitted_at=created_record["submitted_at"],
                updated_at=created_record["updated_at"],
                provider_id=UUID(created_record["provider_id"])
            )
        except Exception as e:
            logger.error(f"Error creating auth request: {str(e)}")
            # Print the full error details
            import traceback
            logger.error(f"Full error traceback: {traceback.format_exc()}")
            raise Exception(f"Failed to create auth request: {str(e)}")

    def get_auth_requests(self, provider_id: UUID) -> List[AuthRequestResponse]:
        try:
            # Query Supabase with RLS enabled
            response = (
                supabase.table("auth_requests")
                .select("*")
                .eq("provider_id", str(provider_id))
                .execute()
            )

            # Convert to response models
            return [
                AuthRequestResponse(
                    id=UUID(record["id"]),
                    patient_name=record["patient_name"],
                    patient_id=record["patient_id"],
                    procedure_code=record["procedure_code"],
                    procedure_description=record["procedure_description"],
                    diagnosis_code=record["diagnosis_code"],
                    diagnosis_description=record["diagnosis_description"],
                    medical_justification=record["medical_justification"],
                    priority=record["priority"],
                    payer_name=record.get("payer_name"),
                    payer_id=record.get("payer_id"),
                    status=record["status"],
                    submitted_at=record["submitted_at"],
                    updated_at=record["updated_at"],
                    provider_id=UUID(record["provider_id"])
                )
                for record in response.data
            ]
        except Exception as e:
            print(f"Error getting auth requests: {str(e)}")
            raise

    def get_auth_request(self, request_id: UUID) -> Optional[AuthRequestResponse]:
        try:
            # Query Supabase with RLS enabled
            response = (
                supabase.table("auth_requests")
                .select("*")
                .eq("id", str(request_id))
                .execute()
            )

            if not response.data:
                return None

            record = response.data[0]
            return AuthRequestResponse(
                id=UUID(record["id"]),
                patient_name=record["patient_name"],
                patient_id=record["patient_id"],
                procedure_code=record["procedure_code"],
                procedure_description=record["procedure_description"],
                diagnosis_code=record["diagnosis_code"],
                diagnosis_description=record["diagnosis_description"],
                medical_justification=record["medical_justification"],
                priority=record["priority"],
                payer_name=record.get("payer_name"),
                payer_id=record.get("payer_id"),
                status=record["status"],
                submitted_at=record["submitted_at"],
                updated_at=record["updated_at"],
                provider_id=UUID(record["provider_id"])
            )
        except Exception as e:
            print(f"Error getting auth request: {str(e)}")
            raise

    def update_auth_request_status(self, request_id: UUID, status: str) -> Optional[AuthRequestResponse]:
        try:
            # Update in Supabase with RLS enabled
            response = (
                supabase.table("auth_requests")
                .update({"status": status, "updated_at": datetime.utcnow().isoformat()})
                .eq("id", str(request_id))
                .execute()
            )

            if not response.data:
                return None

            record = response.data[0]
            return AuthRequestResponse(
                id=UUID(record["id"]),
                patient_name=record["patient_name"],
                patient_id=record["patient_id"],
                procedure_code=record["procedure_code"],
                procedure_description=record["procedure_description"],
                diagnosis_code=record["diagnosis_code"],
                diagnosis_description=record["diagnosis_description"],
                medical_justification=record["medical_justification"],
                priority=record["priority"],
                payer_name=record.get("payer_name"),
                payer_id=record.get("payer_id"),
                status=record["status"],
                submitted_at=record["submitted_at"],
                updated_at=record["updated_at"],
                provider_id=UUID(record["provider_id"])
            )
        except Exception as e:
            print(f"Error updating auth request status: {str(e)}")
            raise 