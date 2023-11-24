from fastapi import HTTPException, status
from routers import router

from models.support import Support
from modules.jwt_token import create_jwt, password_hash

description = "Status: 'aberto', 'resolvido', 'aguardando'"

@router.post("/support", status_code = 201, response_model = dict, description = description)
async def support(body: Support):
    return {}
