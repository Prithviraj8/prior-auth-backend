from fastapi import APIRouter, HTTPException, Header, Depends
from typing import List, Optional
from uuid import UUID
from datetime import datetime
import logging
import jwt

from ....models.auth_request import AuthRequestCreate, AuthRequestResponse
from ....services.auth_request_service import AuthRequestService
from ....database.session import supabase, SUPABASE_SERVICE_KEY

router = APIRouter()
auth_request_service = AuthRequestService()
logger = logging.getLogger(__name__)

# Fixed UUID for service role user
SERVICE_ROLE_USER_ID = "00000000-0000-0000-0000-000000000001"

async def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    try:
        token = authorization.split(" ")[1]
        logger.debug(f"Received token: {token[:10]}...")
        
        # For service role token, use the fixed UUID
        if SUPABASE_SERVICE_KEY and token == SUPABASE_SERVICE_KEY:
            logger.debug("Using service role token")
            return {"id": SERVICE_ROLE_USER_ID, "role": "service_role"}
            
        # For user tokens, set the session and verify
        try:
            logger.debug("Attempting to set session and get user")
            supabase.auth.set_session(token, token)
            user = supabase.auth.get_user()
            if user and user.user:
                logger.debug(f"Found user with ID: {user.user.id}")
                return user.user
            else:
                raise HTTPException(status_code=401, detail="Invalid user token")
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            raise HTTPException(status_code=401, detail=f"Invalid user token: {str(e)}")
            
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Authentication error: {str(e)}")

@router.post("/", response_model=AuthRequestResponse)
async def create_auth_request(
    request: AuthRequestCreate,
    user = Depends(get_current_user)
) -> AuthRequestResponse:
    try:
        logger.debug(f"Creating auth request with user: {user}")
        return auth_request_service.create_auth_request(request, user)
    except Exception as e:
        logger.error(f"Error creating auth request: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[AuthRequestResponse])
async def get_auth_requests(
    provider_id: UUID,
    user = Depends(get_current_user)
) -> List[AuthRequestResponse]:
    try:
        return auth_request_service.get_auth_requests(provider_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{request_id}", response_model=AuthRequestResponse)
async def get_auth_request(
    request_id: UUID,
    user = Depends(get_current_user)
) -> AuthRequestResponse:
    try:
        request = auth_request_service.get_auth_request(request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Authorization request not found")
        return request
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{request_id}/status", response_model=AuthRequestResponse)
async def update_auth_request_status(
    request_id: UUID,
    status: str,
    user = Depends(get_current_user)
) -> AuthRequestResponse:
    try:
        request = auth_request_service.update_auth_request_status(request_id, status)
        if not request:
            raise HTTPException(status_code=404, detail="Authorization request not found")
        return request
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 