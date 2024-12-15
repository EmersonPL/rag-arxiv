## Setup

### 1. Create Docker
Run ```docker compose up``` to setup the database.

To check that the command worked, run ```docker exec -it CONTAINER_NAME psql -hlocalhost -p5432 --username=admin --password --dbname=rag_arxiv```

### 2. Setup Python
Run ```poetry install```. This should install all required dependencies.

### 3. Create .env values
Copy the file ```.env_template```, with name ```.env```, and update the `GEMINI_API_KEY` to br your key.

The other variables may be changed, however the pipeline is only implemented for Gemini models.

### 4. Create Database
To create the database, with the postgres docker container running, run the script
```rag_arxiv/scripts/migrations/create_db.py```.

### 5. Add papers to DB
Run the script ```rag_arxiv/scripts/insert_papers.py```.

The files must be available on a directory ```data/cs_AI``` 
(temporarily, it's expected to run only for cs_AI arxiv papers).

This directory must contain a directory for each paper, named with its code, 
and should contain two files `abstract.json` and `article.pdf`

## Run queries

To run the queries, you can either import the function `rag` from `rag_arxiv/rag_query.py` 
or run the script `rag_arxiv/scripts/query_llm.py`.

To run the function, it should be called with a single positional argument, that's the query to make.

To run the script, it should contain a single argument, with the query 
(`python rag_arxiv/scripts/query_llm.py "Your query here"`)


## Notes
 - The queries are supposed to be written in english.
 - Currently, only works to query for cs_AI Arxiv papers.