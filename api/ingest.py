''' 
This module has the function(s) to index the FAQ data into a search engine.
'''

import json
import minsearch

def load_index(clean_data_path='data/cleaned_data.json'):
    ''' 
    This function loads the cleaned-up data and indexes in the minsearch
    search engine
    '''

    # load the cleaned up json file
    with open(clean_data_path, 'rt',encoding="utf-8") as f_in:
        docs_raw = json.load(f_in)

    # add the actual course (only one is ASU online) to the question-level info
    documents = []
    for did, doc in enumerate(docs_raw['documents']):
        doc['id'] = did #set up a unique id
        doc['course'] = docs_raw['course']
        documents.append(doc)

    # setup data indexing using minsearch
    index = minsearch.Index(
        text_fields=["question", "text", "section"],
        keyword_fields=["course","id"]
    )

    #actually index the data
    index.fit(documents)

    return index
