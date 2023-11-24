from pydantic import BaseModel, Field
from enum import Enum

class StatusEnum(str, Enum):
    aberto = 'aberto'
    resolvido = 'resolvido'
    aguardando = 'aguardando'
    
class Support(BaseModel):
    id: int
    name_student: str
    name_responsible: str
    email_responsible: str
    description: str
    status: StatusEnum 
    date: int