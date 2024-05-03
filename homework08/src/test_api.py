#!/usr/bin/env python3

import pytest
import requests
import api

# Functions

def test_fetch_data():
    test_bool = api.fetch_data()
    assert isinstance(test_bool, bool)
    assert test_bool == True

def test_get_all_data():
    test_dict = api.get_all_data()
    assert isinstance(test_dict, dict)
    assert len(test_dict) > 0

def test_get_gene_ids():
    test_list = api.get_gene_ids()
    assert isinstance(test_list, list)
    assert len(test_list) > 0

def test_get_gene_data():
    test_dict = api.get_gene_data('HGNC:11501')
    assert isinstance(test_dict, dict)
    assert len(test_dict) > 0

def test_delete_all_data():
    test_bool = api.delete_all_data()
    assert isinstance(test_bool, bool)
    assert test_bool == True

# Flask Routes
# Data

def test_route_data_post():
    response1 = requests.post('http://localhost:5000/data')
    assert response1.status_code == 200

def test_route_data_get():
    response1 = requests.get('http://localhost:5000/data')
    assert response1.status_code == 200
    assert isinstance(response1.json(), dict)

# Deleting handled below

# Genes

def test_route_genes_get():
    response1 = requests.get('http://localhost:5000/genes')
    assert response1.status_code == 200
    assert isinstance(response1.json(), list) #list of dicts

def test_route_genes_id_get():
    hgnc_id = 'HGNC:11501'
    response1 = requests.get(f'http://localhost:5000/genes/{hgnc_id}')
    assert response1.status_code == 200
    assert isinstance(response1.json(), dict)

# Jobs

def test_route_jobs_post():
    data = {
    "hgnc_id": "HGNC:11501",
    "count": 5
    }
    response1 = requests.post('http://localhost:5000/jobs', json=data)
    assert response1.status_code == 200
    assert isinstance(response1.json(), dict)

def test_route_jobs_get():
    response1 = requests.get('http://localhost:5000/jobs')
    assert response1.status_code == 200
    assert isinstance(response1.json(), list)

def test_route_jobs_id_get():
    # not sure on this implementation
    jid = 'INVALID_TESTING_UUID'
    response1 = requests.get(f'http://localhost:5000/genes/{jid}')
    assert response1.status_code == 404

# Results

def test_route_results_id_get():
    jid = 'INVALID_TESTING_UUID'
    response1 = requests.get(f'http://localhost:5000/results/{jid}')
    assert response1.status_code == 404

def test_route_data_delete():
    response1 = requests.delete('http://localhost:5000/data')
    assert response1.status_code == 200
