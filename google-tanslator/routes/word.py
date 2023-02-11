from fastapi import APIRouter
from fastapi.params import Param
from bson import ObjectId
from enum import IntEnum

from models.word import *
from models.language import *
from schemas.word import *
from configs.db import conx
from utils.parsers import get_data

word = APIRouter()

class Option(IntEnum):
    T = 1
    F = 0

class Sorting(IntEnum):
    AS = 1
    DS = -1

@word.get("/word/{id}")
async def get_word_details(word_tf: str, dest: Language):
    one_word = word_tf.split()[0]
    response = conx.google_translator.word.find_one({"word":one_word, "dest": dest})

    if response:
        return(serializerDict(response))

    new_word = await get_data(one_word, dest)
    conx.google_translator.word.insert_one(dict(new_word))
    
    return serializerDict(conx.google_translator.word.find_one({"word":one_word, "dest": dest}))

@word.get("/words/")
async def find_all_words( word: str, pagin: int = 10, trans: Option = 0, data: Option = 0, sort: Sorting = 1 ):

    if trans == 1 and data == 0:
        return serializerList(conx.google_translator.word.aggregate([
            { '$match'    : { "word" : {'$regex': word }} },
            { '$project' : { '_id' : 1, 
                        'word' : 1,
                        'translated': 1}},
            { '$sort'     : { 'word' : sort } },
            { '$skip': pagin * 2},
            { '$limit': pagin }
            ]))
    if trans == 0 and data == 1:
        return serializerList(conx.google_translator.word.aggregate([
        { '$match'    : { "word" : {'$regex': word }} },
        { '$project' : { '_id' : 1, 
                        'word' : 1,
                        'data':1}},
        { '$sort'     : { 'word' : sort } },
        { '$skip': pagin * 2},
        { '$limit': pagin }
        ] ))
    if data == 1 and trans == 1:
        return serializerList(conx.google_translator.word.aggregate([
        { '$match'    : { "word" : {'$regex': word }} },
        { '$project' : { '_id' : 1, 
                        'word' : 1,
                        'translated': 1,
                        'data':1}},
        { '$sort'     : { 'word' : sort } },
        { '$skip': pagin * 2},
        { '$limit': pagin }
        ] ))
    
    return serializerList(conx.google_translator.word.aggregate([
        { '$match'    : { "word" : {'$regex': word }} },
        { '$project' : { '_id' : 1, 
                        'word' : 1}},
        { '$sort'     : { 'word' : sort } },
        { '$skip': pagin * 2},
        { '$limit': pagin }
    ] ))


@word.delete("/delete/{id}")
async def delete_word(id):
    return serializerDict(conx.google_translator.word.find_one_and_delete({"_id": ObjectId(id)}))

@word.get("/{id}")
async def find_one_word(id):
    return serializerDict(conx.google_translator.word.find_one({"_id": ObjectId(id)}))

@word.post("/")
async def create_word(word: Word):
    conx.google_translator.word.insert_one(dict(word))
    return serializerDict(conx.google_translator.word.find())

@word.put("/{id}")
async def update_word(id, word: Word):
    conx.google_translator.word.find_one_and_update({"_id": ObjectId(id)},{"$set":dict(word)})
    return serializerDict(conx.google_translator.word.find_one({"_id": ObjectId(id)}))