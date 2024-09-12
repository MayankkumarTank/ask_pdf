from pydantic import BaseModel

class Prompt(BaseModel):
    type: str
    content: str