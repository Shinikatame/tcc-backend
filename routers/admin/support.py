from fastapi import HTTPException, status
from routers.admin import router

from typing import List

from models.support import SupportResponse
from database.support import SupportORM
    
@router.get("/support", response_model = List[SupportResponse])
async def get_supports():
    supports = await SupportORM.find_many()
    response = [SupportResponse(**s.dict()) for s in supports if isinstance(s.dict(), dict)]
    return response


@router.get("/support/{support_id}", response_model = SupportResponse)
async def get_support(support_id: int):
    support = await SupportORM.find_one(id = support_id)
    if not support:
        raise HTTPException(status_code = 404, detail = 'Suporte não encontrado')
    return SupportResponse(**support.dict())


@router.patch("/support/{support_id}", response_model = SupportResponse)
async def student_edit(support_id: int, status: str):
    support = await SupportORM.update(support_id, status = status)
    if not support:
        raise HTTPException(status_code = 404, detail = 'Suporte não encontrado')
    return SupportResponse(**support.dict())
