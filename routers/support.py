from fastapi import HTTPException, status, Header
from routers import router

from datetime import datetime

from models.support import Support, SupportResponse
from database.support import SupportORM
from modules.jwt_token import verify_jwt

description = "Status: 'aberto', 'resolvido', 'aguardando'"
    
@router.post("/support", status_code = 201, response_model = SupportResponse, description = description)
async def support(parms: Support, Authorization: str = Header(None)):
    if not Authorization or not Authorization.startswith("Bearer "):
        detail = 'Cabeçalho "Authorization" não especificado na solicitação' if not Authorization else 'Token JWT inválido'
        raise HTTPException(status_code = 401, detail = detail)

    token = Authorization.replace('Bearer ', '')
    user = await verify_jwt(token)
    
    data = parms.dict()
    data['name_student'] = user.name
    data['name_responsible'] = user.name_responsible
    data['email_responsible'] = user.email_responsible
    data['date'] = int(datetime.now().timestamp())

    support = await SupportORM.create(**data)
    response = SupportResponse(**support.dict())
    return response
