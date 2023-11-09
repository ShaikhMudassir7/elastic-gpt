# Elasticsearch-ChatGPT

## Installation

### Clone repo

```sh
git clone https://github.com/ashishtiwari1993/elasticsearch-chatgpt.git
cd elasticsearch-chatgpt
```

### Replace credentials

Open `Dockerfile` and change below creds

```sh
ENV openai_api="<open_api_key>"
ENV cloud_id="<elastic cloud id>"
ENV cloud_user="elastic"
ENV cloud_pass="<elastic_cloud_password>"
ENV es_index="<elasticsearch_index_name>"
ENV chat_title="<Any title for your page e.g. ashish.one GPT>"
ENV vector_field="< specify vector field where embedding will be save. e.g. title-vector>"
```

### Build

```sh
docker build -t es-gpt .
```

### Run

```sh
docker run -p 8501:8501 es-gpt
```

Simply visit on [localhost:8501](localhost:8501)

## Reference
[Blog - ChatGPT and Elasticsearch: OpenAI meets private data](https://www.elastic.co/blog/chatgpt-elasticsearch-openai-meets-private-data)
