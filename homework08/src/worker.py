import logging
import json
from jobs import get_job_by_id, update_job_status, q, rd, results
from api import get_gene_data, get_gene_ids
import time

def get_same_group_ids(hgnc_id, count):
    hgnc_data = get_gene_data(hgnc_id)
    logging.error(hgnc_data)
    try:
        group = hgnc_data['gene_group'][0]
    except Exception as e:
        logging.error("Gene has no group")
        return [hgnc_id]

    if group is not None:

        logging.info(f"Searching for group {group}")

        gene_ids = get_gene_ids()
        same_group_ids = []
        for gene_id in gene_ids:
            try:
                test_group = get_genet_data(gene_id)['gene_group'][0]
            except Exception as e:
                continue
            if (gene_id != hgnc_id) and (test_group == group):
                logging.info(f"Found gene {gene_id}")
                same_group_ids.append(gene_id)

    selected_ids = same_group_ids[:count]

    return selected_ids


@q.worker
def do_work(jobid):
    logging.info("Worker started")
    update_job_status(jobid, 'in progress')

    job = get_job_by_id(jobid)
    hgnc_id = job['hgnc_id']
    count = job['count']

    selected_ids = get_same_group_ids(hgnc_id, count)
    results.set(jobid, json.dumps(selected_ids))
    logging.info(f"Worker complete, found {len(selected_ids)} matching genes")

    update_job_status(jobid, 'complete')

do_work()
