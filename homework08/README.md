# Human Genome Project Redis/Flask App

## Overview

This project involves fetching data from the HGNC website and storing the data in a Redis database using Python. This is also a Flask app, enabling data to be requested and sent over the internet. The data can be accessed from this link, however the program will access it automatically: https://g-a8b222.dd271.03c0.data.globus.org/pub/databases/genenames/hgnc/json/hgnc_complete_set.json

### Scripts
- `gene_api.py`
This script contains functions for fetching and managing the data, alongside creating the Flask app.
#### Functions
- The `fetch_data()` function fetches the genome data from HGNC's website.
- The `get_all_data()` function returns all data from the Redis database.
- The `delete_all_data()` function deletes all data in the Redis database.
- The `get_gene_ids()` function grabs all hgnc_id entries in the Redis database.
- The `get_gene_data()` function grabs all data for a specific hgnc_id entry in the Redis database.

### Running the Code (Containerized)
1. Make sure Docker & Redis are intalled on your computer
2. Download or clone this repository into a directory.
3. In the directory, run `docker-compose up` And wait for the Docker images to generate and for the Flask app to start.
4. To check things are up and running, in a separate terminal window run `docker ps -a`
5. See Flask Interaction below

### Flask Interaction
You can interact with the flask app via `curl -X <method> "localhost:5000/<route>"` once it is up and running.
IMPORTANT: Make sure to `curl -X POST "localhost:5000/data"` before trying to access the other methods and test scripts. Nothing will break, however you wont get any data returned as the database would be empty otherwise.

#### Routes
| Route              | Method   | Description                                   |
|--------------------|----------|-----------------------------------------------|
| `/data`            | `POST`   | Posts data into Redis                         |
| `/data`            | `GET`    | Returns all data from Redis                   |
| `/data`            | `DELETE` | Deletes data in Redis                         |
| `/genes`           | `GET`    | Return JSON-formatted list of all hgnc_ids    |
| `/genes/<hgnc_id>` | `GET`    | Return all data associated with `<hgnc_id>`   |
| `/jobs`            | `POST`   | Create a new job with a unique job ID         |
| `/jobs`            | `GET`    | List all existing job IDs                     |
| `/jobs/<jobid>`    | `GET`    | Return job information for given `<jobid>`    |

#### Raw Example

```
curl -X POST "localhost:5000/data"
curl -X GET "localhost:5000/genes/HGNC:11501"
```

Will return:

```
{
  ...
  "date_approved_reserved": "1999-03-19",
  "date_modified": "2023-01-20",
  ...
  "gene_group": [
    "Synaptogyrins"
  ],
  "gene_group_id": [
    1475
  ],
  "hgnc_id": "HGNC:11501",
  "location": "16p13.3",
  "location_sortable": "16p13.3",
  "locus_group": "protein-coding gene",
  "locus_type": "gene with protein product",
  ...
  "name": "synaptogyrin 3",
  ...
  "status": "Approved",
  "symbol": "SYNGR3",
  ...
}

```

#### Job Example
```
curl -X POST "localhost:5000/jobs" -H "Content-Type: application/json" -d '{"hgnc_id": "HGNC:11501", "count": 5}'
curl -X GET "localhost:5000/results/<JOB ID>"
```

Will return a list of the 3 known synaptogyrins in humans.
```
["HGNC:11499", "HGNC:11500", "HGNC:11501"]
```

### Data Interpretation
Not all fields are included, however here are the basics:
- `hgnc_id`: Unique gene ID. All approved entries should have this field.
- `symbol`: HGNC approved gene symbol.
- `status`: Status of the symbol report
- `name`: HGNC approved name for the gene
- `location`: Cytogenetic location of the gene
- `gene_group` / `gene_family` Name of the group or family the gene has been assigned to.

