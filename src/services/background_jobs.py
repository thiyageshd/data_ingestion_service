import random
import string
from redis import Redis
from rq import Queue
from kafka import KafkaProducer
from src.utils.helpers import fetch_and_store_data
from src.config import Config
import json
from loguru import logger

class BackgroundJobService:
    def __init__(self):
        self.redis_conn = Redis.from_url(Config.REDIS_URL)
        self.queue = Queue(connection=self.redis_conn)
        self.producer = KafkaProducer(
            bootstrap_servers=Config.KAFKA_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def schedule_fetching_job(self, symbol: str) -> str:
        job_id = self._generate_job_id()
        self.queue.enqueue(self.process_financial_data, symbol, job_id)
        return job_id

    def process_financial_data(self, symbol: str, job_id: str):
        """ Fetch financial data and send it to Kafka. """
        try:
            result = fetch_and_store_data(symbol, job_id)
            if result:
                self.send_to_kafka(Config.KAFKA_TOPIC, result)  # Send result to Kafka
        except Exception as e:
            logger.error(f"Error processing financial data: {e}")


    def send_to_kafka(self, topic: str, data: dict):
        """ Serializes data and sends it to a Kafka topic. """
        try:
            message = json.dumps(data)
            self.producer.send(topic, message.encode("utf-8"))
            self.producer.flush()  # Ensures the message is sent immediately
        except Exception as e:
            logger.error(f"Error sending message to Kafka: {e}")

    def delivery_report(self, err, msg):
        """ Callback for Kafka message delivery. """
        if err:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")



    def get_job_status(self, job_id: str) -> str:
        job = self.queue.fetch_job(job_id)
        if job:
            return job.get_status()
        return "unknown"

    def _generate_job_id(self) -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))