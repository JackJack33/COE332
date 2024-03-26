# Human Genome Project Redis/Flask App

## Overview

This project involves fetching data from the HGNC website and storing the data in a Redis database using Python. This is also a Flask app, enabling data to be requested and sent over the internet. The data can be accessed from this link, however the program will access it automatically: https://g-a8b222.dd271.03c0.data.globus.org/pub/databases/genenames/hgnc/json/hgnc_complete_set.json

### Scripts
`gene_api.py`
This script contains functions for fetching and managing the data, alongside creating the Flask app. Functions include `fetch_data()`, `get_all_data()`, `delete_all_data()`, `get_gene_ids()`, and `get_gene_data()`

### Running the Code (Containerized)
1. Make sure Docker & Redis are intalled on your computer
2. Download or clone this repository into a directory.
3. In the directory, run `docker-compose up` And wait for the Docker image to generate and for the Flask app to start.
4. To check things are up and running, in a separate terminal window run `docker ps -a`
5. See Flask Interaction below

### Flask Interaction
You can interact with the flask app via `curl -X <method> localhost:5000/<route>` once it is up and running.

| Route            | Method | Description                              |
|------------------|--------|-----------------------------------------------|
| /data            | POST   | Posts data into Redis                           |
| /data            | GET    | Returns all data from Redis                    |
| /data            | DELETE | Deletes data in Redis                          |
| /genes           | GET    | Return JSON-formatted list of all hgnc_ids    |
| /genes/<hgnc_id> | GET    | Return all data associated with `<hgnc_id>`    |


### Interpretation
- The `fetch_data()` function fetches the genome data from HGNC's website.
- The `get_all_data()` function returns all data from the Redis database.
- The `delete_all_data()` function deletes all data in the Redis database.
- The `get_gene_ids()` function grabs all hgnc_id entries in the Redis database.
- The `get_gene_data()` function grabs all data for a specific hgnc_id entry in the Redis database.