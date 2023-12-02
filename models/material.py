from pydantic import BaseModel

class Material(BaseModel):
    file: str


class MaterialResponse(Material):
    id: int
    course_id: int