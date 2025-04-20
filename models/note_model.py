from pydantic import BaseModel

class Note(BaseModel):
    id: int
    title: str
    desc: str
    isImp: bool = False