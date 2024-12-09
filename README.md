## Setup
Run ```docker compose up``` to setup the database.

To check that the command worked, run ```docker exec -it CONTAINER_NAME psql -hlocalhost -p5432 --username=admin --password --dbname=rag_arxiv```
