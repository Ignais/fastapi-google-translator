
import googletrans
from googletrans import *

import numpy as np 
from collections import defaultdict

trans = Translator()

"""
El Parse se puede hacer a mayor profundidad para lograr alcanzar mas datos.
"""


async def get_data(word: str, dest: str) -> dict:
    
    word_translated = trans.translate(word, dest)
    word_origin = word
    translations = word_translated.text
    dest_t = word_translated.dest
    extra_data = dict(enumerate(np.array(word_translated.extra_data["parsed"], dtype=object)))
    
    mapper = {}
    if len(extra_data) > 3:
        syn_trnaslated = extra_data[3]

        keys = ["original","origin_data","other_examples","data_1","data_2","other_transl",
                "data_3","data_4","origin_lang","data_5"]

        temp = [{key : val for key, val in zip(keys, syn_trnaslated)}]

        res = defaultdict(list)
        {res[key].append(sub[key]) for sub in temp for key in sub}

        datas = dict(res)
    
        origin_data = dict(enumerate(datas['origin_data']))
    
        origin_data_pars = dict(enumerate(origin_data[0]))
        parse = dict(enumerate(origin_data_pars[0]))
        for i in range(len(parse)):
            if len(parse[i][1][0]) > 3:
                mapper.update({parse[i][0]:{"definitions":parse[i][1][0][0],
                                        "examples":parse[i][1][0][1],
                                        "synonyms":parse[i][1][0][5][0]}})
            else:
                mapper.update({parse[i][0]:{"definitions":parse[i][1][0][0],
                                            "examples":parse[i][1][0][1]}})
 
    return {"word": word_origin.lower(),
            "translated": translations.lower(),
            "dest": dest_t.lower(),
            "data":mapper}