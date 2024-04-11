from jobs import get_job_by_id, update_job_status, q, rd
import time

@q.worker
def do_work(jobid):
    update_job_status(jobid, 'in progress')
    time.sleep(10)   # rd.get() .... do some analysis
    update_job_status(jobid, 'complete')

do_work()
