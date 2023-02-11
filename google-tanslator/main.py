from fastapi import FastAPI

from models.word import Word
from routes.word import word

description = '''
Microservice providing an API to work with word definitions/translations 
taken from Google Translate.
'''

app = FastAPI(
    title="Challenge",
    description=description,
    version="0.0.1",
    contact={
        "name": "Ignais La Paz Trujillo",
        "email": "ignais@gmail.com",
    },
)
app.include_router(word)