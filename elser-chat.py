import os
import streamlit as st
import openai
from elasticsearch import Elasticsearch

# This code is part of an Elastic Blog showing how to combine
# Elasticsearch's search relevancy power with 
# OpenAI's GPT's Question Answering power
# https://www.elastic.co/blog/chatgpt-elasticsearch-openai-meets-private-data

# Code is presented for demo purposes but should not be used in production
# You may encounter exceptions which are not handled in the code


openai_api = os.environ['openai_api']
cloud_id = os.environ['cloud_id']
cloud_user = os.environ['cloud_user']
cloud_pass = os.environ['cloud_pass']
es_index = os.environ['es_index']
chat_title = os.environ['chat_title']


openai.api_key = openai_api
model = "gpt-3.5-turbo-0301"

# Connect to Elastic Cloud cluster
def es_connect(cid, user, passwd):
    es = Elasticsearch(cloud_id=cid, basic_auth=(user, passwd))
    print(es)
    return es

# Search ElasticSearch index and return body and URL of the result
def search(query_text):
    cid = cloud_id
    cp = cloud_pass
    cu = cloud_user
    es = es_connect(cid, cu, cp)

    # Elasticsearch query (BM25) and elser(text_expansion) configuration for hybrid search

    query = {
            "bool": { 
              "should": [
                {
                  "text_expansion": {
                    "ml.inference.title_expanded.predicted_value": {
                      "model_text": query_text,
                      "model_id": ".elser_model_1",
                      "boost": 1
                    }
                  }
                },
                {
                  "query_string": {
                    "query": query_text,
                    "default_field": "title",
                    "boost": 4
                  }
                }
              ]
            }
          }


    fields = ["title", "body_content", "url"]
    
    resp = es.search(index=es_index,
                     query=query,
                     fields=fields,
                     size=1,
                     source=False)

    body = resp['hits']['hits'][0]['fields']['body_content'][0]
    url = resp['hits']['hits'][0]['fields']['url'][0]

    return body, url

def truncate_text(text, max_tokens):

    
    tokens = text.split()

    if len(tokens) <= max_tokens:
        return text

    return ' '.join(tokens[:max_tokens])

# Generate a response from ChatGPT based on the given prompt
def chat_gpt(prompt, model="gpt-3.5-turbo", max_tokens=1024, max_context_tokens=4000, safety_margin=5):
    # Truncate the prompt content to fit within the model's context length
    truncated_prompt = truncate_text(prompt, max_context_tokens - max_tokens - safety_margin)
    print(truncated_prompt)

    response = openai.ChatCompletion.create(model=model, temperature=1, messages=[{"role": "user", "content": truncated_prompt}])
    
    print(response)
    return response["choices"][0]["message"]["content"]


st.title(chat_title)

# Main chat form
with st.form("chat_form"):
    query = st.text_input("You: ")
    submit_button = st.form_submit_button("Send")

# Generate and display response on form submission
negResponse = "I'm unable to answer the question based on the information I have from Elastic."
if submit_button:
    resp, url = search(query)

    #removing garbage text. Not applicable for other case
    resp = ' '.join(resp.split()[30:])
    resp = resp.rsplit(' ', 58)[0]

    prompt = f"Rephrase this content \"{resp}\" according to this search query \"{query}\". If the answer is not contained in the supplied content reply \"{negResponse}\" and nothing else"
    answer = chat_gpt(prompt)
    
    if negResponse in answer:
        st.write(f"ChatGPT: {answer.strip()}")
    else:
        st.write(f"ChatGPT: {answer.strip()}\n\nDocs: {url}")
