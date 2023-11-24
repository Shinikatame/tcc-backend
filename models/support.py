from pydantic import BaseModel, Field
from enum import Enum

class StatusEnum(str, Enum):
    aberto = 'aberto'
    resolvido = 'resolvido'
    aguardando = 'aguardando'
    
class Support(BaseModel):
    name_student: str
    name_responsible: str
    email_responsible: str
    description: str
    status: str 
    date: int


class SupportResponse(Support):
    id: int