import json
import random
import string
from redis import Redis
from rq import Queue
from confluent_kafka import Producer
from loguru import logger

from src.utils.helpers import fetch_and_store_data
from src.config import Config


def process_financial_data(symbol: str, job_id: str):
    """ Fetch financial data and send it to Kafka. """
    try:
        producer = Producer({'bootstrap.servers': Config.KAFKA_SERVERS})
        result = fetch_and_store_data(symbol, job_id)
        if result:
            send_to_kafka(producer, Config.KAFKA_TOPIC, result)  # Send result to Kafka
    except Exception as e:
        logger.error(f"Error processing financial data: {e}")


def send_to_kafka(producer: Producer, topic: str, data: dict):
    """ Serializes data and sends it to a Kafka topic. """
    try:
        message = json.dumps(data)
        producer.produce(topic, message.encode("utf-8"), callback=delivery_report)
        producer.flush()  # Ensures the message is sent immediately
    except Exception as e:
        logger.error(f"Error sending message to Kafka: {e}")

def delivery_report(err, msg):
    """ Callback for Kafka message delivery. """
    if err:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")
        
class BackgroundJobService:
    def __init__(self):
        self.redis_conn = Redis.from_url(Config.REDIS_URL)
        self.queue = Queue("financial_jobs", connection=self.redis_conn)
        
    def schedule_fetching_job(self, symbol: str) -> str:
        job_id = self._generate_job_id()
        self.queue.enqueue(process_financial_data, symbol, job_id)
        return job_id

    def get_job_status(self, job_id: str) -> str:
        job = self.queue.fetch_job(job_id)
        if job:
            return job.get_status()
        return "unknown"

    def _generate_job_id(self) -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    