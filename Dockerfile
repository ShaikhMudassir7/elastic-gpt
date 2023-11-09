FROM python:3.9-slim

COPY . /elasticsearch-chatgpt
WORKDIR /elasticsearch-chatgpt

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENV openai_api="<open_api_key>"
ENV cloud_id="<elastic cloud id>"
ENV cloud_user="elastic"
ENV cloud_pass="<elastic_cloud_password>"
ENV es_index="<elasticsearch_index_name>"
ENV chat_title="<Any title for your page e.g. ashish.one GPT>"

# Comment this variable in case of ELSER. It by default using 'title' field..
#ENV vector_field="< specify vector field where embedding will be save. e.g. title-vector>"

# Change script name to 'elser-chat.py' in case of ELSER.
#ENTRYPOINT ["streamlit", "run", "chat.py", "--server.port=8501", "--server.address=0.0.0.0"]
ENTRYPOINT ["streamlit", "run", "elser-chat.py", "--server.port=8501", "--server.address=0.0.0.0"]
