from pydantic import BaseModel


class Word(BaseModel):
    word: str
    translated: str 
    dest: str
    data: dict


