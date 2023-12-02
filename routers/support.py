from fastapi import HTTPException, status, Depends, Header
from routers import router

from datetime import datetime

from models.support import Support, SupportResponse
from database.support import SupportORM
from modules.jwt_token import has_authenticated

description = "Status: 'aberto', 'resolvido', 'aguardando'"
    
@router.post("/support", status_code = 201, response_model = SupportResponse, description = description)
async def support(parms: Support, user: dict = Depends(has_authenticated)):
    user = await UserORM.find_one(id = user.id)
    
    data = parms.dict()
    data['name_student'] = user.name
    data['name_responsible'] = user.name_responsible
    data['email_responsible'] = user.email_responsible
    data['date'] = int(datetime.now().timestamp())

    support = await SupportORM.create(**data)
    response = SupportResponse(**support.dict())
    return response
