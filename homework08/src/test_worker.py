#!/usr/bin/env python3

import pytest
from worker import get_same_group_ids
from api import get_gene_data

# Functions

def test_get_same_group_ids():
    hgnc_id = 'HGNC:11501'
    count = 5
    group = get_gene_data(hgnc_id).get('group')

    selected_ids = get_same_group_ids(hgnc_id, count)
    assert len(selected_ids) <= count

    for gene_id in selected_ids:
        assert get_gene_data(gene_id).get('group') == group
