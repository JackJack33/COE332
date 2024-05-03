#!/usr/bin/env python3

import json
import pytest
from worker import get_same_group_ids
from api import get_gene_data

# Functions

def test_get_same_group_ids():
    hgnc_id = 'HGNC:11501'
    count = 5
    hgnc_data = get_gene_data(hgnc_id)
    group = hgnc_data['gene_group'][0]

    selected_ids = get_same_group_ids(hgnc_id, count)
    assert len(selected_ids) <= count
