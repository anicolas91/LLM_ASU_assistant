''' 
This module contains all the functions needed to perform
Retreval Augmented Generation (RAG) using ASU online's FAQ
database.
'''

import os
import ingest
from dotenv import load_dotenv
from openai import OpenAI

# setup API key
load_dotenv('../.envrc') 
openai_api_key = os.getenv('OPENAI_API_KEY')

# start an openAI client
client = OpenAI()

# index the data
index = ingest.load_index()

# set up RAG definitions
def search(query,boost=None):
    '''
    This function retrieves the top 5 results from an indexed search enging.
    We are using a homemade engine called 'minsearch' which has been
    developed by alexey grigorev.
    '''
    if boost is None:
        boost = {'question': 3.0, 'section': 0.5}

    results = index.search(
        query = query,
        filter_dict={'course':'ASU Online'}, #this is a bit moo, but done for continuity
        boost_dict=boost,
        num_results=10
        )
    
    return results

def build_prompt(query,search_results):
    '''  
    This function creates an LLM friendly prompt using the results from a search engine
    as background information input.
    '''
    prompt_template = """ 
    You are a course teaching assistant. Please answer the QUESTION based on the CONTEXT from the FAQ database.
    Use only the facts from the CONTEXT when answering the QUESTION.

    QUESTION: {question}

    CONTEXT: {context}

    """.strip()

    context= ""

    # concatenate search results as one text string
    for doc in search_results:
        context = context + f'section: {doc['section']} \nquestion: {doc['question']} \nanswer: {doc['text']}\n\n'

    # fill out the prompt template
    prompt = prompt_template.format(question=query, context=context).strip()

    return prompt

def llm(prompt,model='gpt-4o-mini'):
    '''  
    This function contacts sets up the LLM model and runs the formatted prompt
    '''
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content
    
# set up the RAG using the 3 steps above
def rag(query,model='gpt-4o-mini',boost=None):
    ''' 
    This function generates a Retrieval-Augmented generation model architecture.
    It combines search engine retrieval results with LLM to give a user-friendly answer.
    '''
    search_results = search(query,boost=boost)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt,model=model)
    return answer
