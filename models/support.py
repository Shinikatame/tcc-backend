from pydantic import BaseModel, Field
from enum import Enum

class StatusEnum(str, Enum):
    aberto = 'aberto'
    resolvido = 'resolvido'
    aguardando = 'aguardando'
    
class Support(BaseModel):
    description: str
    status: str 


class SupportResponse(Support):
    id: int
    name_student: str
    name_responsible: str
    email_responsible: str
    date: int