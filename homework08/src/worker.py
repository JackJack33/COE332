from jobs import get_job_by_id, update_job_status, q, rd
from api import get_gene_data, get_gene_ids
import time

def get_same_group_ids(hgnc_id, count):
    hgnc_data = get_gene_data(hgnc_id)
    group = hgnc_data['gene_group']

    gene_ids = get_gene_ids()
    same_group_ids = [gene_id for gene_id in gene_ids
                      if (gene_id != hgnc_id) and
                      get_gene_data(gene_id)['gene_group'] == group]
    selected_ids = same_group_ids[:count]

    return selected_ids


@q.worker
def do_work(jobid):
    update_job_status(jobid, 'in progress')

    job = get_job_by_id(jobid)
    hgnc_id = job['hgnc_id']
    count = job['count']

    selected_ids = get_same_group_ids(hgnc_id, count)
    results.set(jobid, json.dumps(selected_ids))

    update_job_status(jobid, 'complete')

do_work()
