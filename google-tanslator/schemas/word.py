
def wordEntity(item) -> dict:
    return{
        "id": str(item["_id"]),
        "word": item["word"],
        "translated": item["translated"], 
        "dest": item["dest"],
        "data": dict(item["data"])
    }

def wordsEntity(entity) -> list:
    return [wordEntity(item) for item in entity]

def serializerDict(a) -> dict:
    return{**{ i:str(a[i]) for i in a if i == "_id"},**{i:a[i] for i in a if i != "_id"}}

def serializerList(entity) -> list:
    return [serializerDict(a) for a in entity]