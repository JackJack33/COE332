#!/usr/bin/env python3

import pytest
import uuid
from jobs import add_job, get_job_by_id, get_results_by_id, get_all_job_ids, update_job_status

# Functions

def test_add_job():
    job = add_job("test_start", "test_end", jid="test_jid")
    assert job['status'] == "submitted"

def test_get_job_by_id():
    job = get_job_by_id("test_jid")
    assert job is not None
    assert job['status'] is not None

def test_get_all_job_ids():
    job_ids = get_all_job_ids()
    assert isinstance(job_ids, str)
    assert "test_jid" in job_ids

def test_update_job_status():
    update_job_status("test_jid", "completed")
    job = get_job_by_id("test_jid")
    assert job['status'] == "completed"
