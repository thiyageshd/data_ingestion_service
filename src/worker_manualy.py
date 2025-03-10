from rq import Queue
from rq.job import Job
from redis import Redis
from src.services.background_jobs import process_financial_data

redis_conn = Redis.from_url("redis://localhost:6379")
queue = Queue("financial_jobs", connection=redis_conn)

# job = queue.fetch_job("X6EW09LUJV")
# print(job.exc_info)

# if job:
#     process_financial_data(*job.args)  # Run the function manually

failed_jobs = queue.failed_job_registry.get_job_ids()
print("Failed Jobs:", failed_jobs)

# Print error details for each failed job
for job_id in failed_jobs:
    job = Job.fetch(job_id, connection=redis_conn)
    print(f"Job ID: {job_id}")
    print(f"Error: {job.exc_info}")  # Print error traceback