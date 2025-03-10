from rq import Queue
from rq.worker import SimpleWorker
from redis import Redis

from src.config import Config

redis_conn = Redis.from_url(Config.REDIS_URL)
queue = Queue("financial_jobs", connection=redis_conn)

worker = SimpleWorker([queue], connection=redis_conn)
worker.work()

