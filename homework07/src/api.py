#!/usr/bin/env python3
import os
import json
import requests
import logging
import redis
from typing import Dict, List, Any, Tuple
from flask import Flask, request, jsonify

import jobs

app = Flask(__name__)
url = "https://g-a8b222.dd271.03c0.data.globus.org/pub/databases/genenames/hgnc/json/hgnc_complete_set.json"
_redis_ip = os.environ.get('REDIS_IP')
_redis_port = 6379
redis_client = redis.Redis(host=_redis_ip, port=_redis_port, db=0)


def fetch_data() -> bool:
    """
    Fetches gene data from the URL and stores it in Redis.

    Returns:
        bool: True if data storage is successful, False if not.
    """
    try:
        response = requests.get(url)
        if (response.status_code != 200):
            raise request.exceptions.RequestException
        data = response.json()

        for doc in data['response']['docs']:
            hgnc_id = doc.get('hgnc_id')
            if hgnc_id:
                redis_client.set(hgnc_id, json.dumps(doc))
            else:
                logging.warning("Missing hgnc_id, omitting from database")

        return True
    except Exception as e:
        logging.error(f"Error fetching data: {e} {response}")
        return False

def get_all_data() -> Dict[str, str]:
    """
    Retrieves all data stored in Redis.

    Returns:
        Dict[str, str]: A dictionary containing all data stored in Redis.
    """
    try:
        keys = redis_client.keys()
        data = {}
        for key in keys:
            data[key.decode()] = redis_client.get(key).decode()
        return data
    except Exception as e:
        logging.error(f"Error retrieving data from Redis: {e}")
        return None

def delete_all_data() -> bool:
    """
    Deletes all data stored in Redis.

    Returns:
        bool: True if all data is successfully deleted from Redis, False if not.
    """
    try:
        keys = redis_client.keys()
        for key in keys:
            redis_client.delete(key)
        return True
    except Exception as e:
        logging.error(f"Error deleting data from Redis: {e}")
        return False

def get_gene_ids() -> List[str]:
    """
    Retrieves all gene IDs stored in Redis.

    Returns:
        List[str]: A list of gene IDs.
    """
    try:
        keys = redis_client.keys()
        return [key.decode() for key in keys]
    except Exception as e:
        logging.error(f"Error fetching gene ids: {e}")
        return None

def get_gene_data(hgnc_id: str) -> Dict[str, str]:
    """
    Retrieves gene data from Redis based on the provided gene ID.

    Args:
        hgnc_id (str): The HGNC ID of the gene.

    Returns:
        dict: Gene data stored in Redis.
    """
    try:
        data = redis_client.get(hgnc_id)
        return json.loads(data.decode())
    except Exception as e:
        logging.error(f"Error fetching gene data: {e} {hgnc_id}")
        return None

@app.route('/data', methods=['POST'])
def post_data():
    if fetch_data():
        return "Stored data in Redis successfully", 200
    return "Failed to store data in Redis", 500

@app.route('/data', methods=['GET'])
def get_data():
    data = get_all_data()
    if data:
        return jsonify(data), 200
    return "Failed to get all data", 500

@app.route('/data', methods=['DELETE'])
def delete_data():
    if delete_all_data():
        return "Successfully deleted all data", 200
    return "Failed to delete all data", 500

@app.route('/genes', methods=['GET'])
def get_genes():
    gene_ids = get_gene_ids()
    if gene_ids:
        return jsonify(gene_ids), 200
    return "Failed to get gene ids", 500

@app.route('/genes/<hgnc_id>', methods=['GET'])
def get_gene(hgnc_id):
    gene_data = get_gene_data(hgnc_id)
    if gene_data:
        return jsonify(gene_data), 200
    return "Gene not found", 404

@app.route('/jobs', methods=['POST'])
def post_job():
    data = request.get_json()
    hgnc_id = data.get('hgnc_id')
    name = data.get('name')
    if hgnc_id is None or name is None:
        return "hgnc_id and name parameters required", 400

    job_dict = jobs.add_job(hgnc_id,name)
    return jsonify(job_dict), 200

@app.route('/jobs', methods=['GET'])
def get_all_jobs():
    try:
        job_ids = jobs.get_all_job_ids()
        return jsonify(job_ids), 200
    except Exception as e:
        return str(e), 500

@app.route('/jobs/<jid>', methods=['GET'])
def get_job(jid):
    try:
        job_dict = jobs.get_job_by_id(jid)
        if job_dict:
            return jsonify(job_dict), 200
        else:
            return "Job not found", 404
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
