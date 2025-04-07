# app/api/code_execution.py

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from app.services.code_execution import CodeExecutionService
from app.services.auth import AuthService

router = APIRouter(prefix="/code", tags=["code execution"])

class CodeExecutionRequest(BaseModel):
    code: str
    expected_output: Optional[str] = None

class CodeExecutionResponse(BaseModel):
    execution_id: str
    success: bool
    output: str
    error: Optional[str] = None
    execution_time: float
    matches_expected: Optional[bool] = None

@router.post("/execute", response_model=CodeExecutionResponse)
async def execute_code(
    request: CodeExecutionRequest,
    current_user = Depends(AuthService().get_current_user)
):
    """
    Execute Python code and return the result.
    This endpoint requires authentication.
    """
    execution_service = CodeExecutionService()
    result = execution_service.execute_code(
        code=request.code,
        expected_output=request.expected_output
    )
    
    return result