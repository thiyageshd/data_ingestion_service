import os

class Config:
    KAFKA_TOPIC = "data_ingestion_topic"
    YAHOO_FINANCE_API_URL = "https://finance.yahoo.com"
    YAHOO_API_KEY = os.getenv("YAHOO_API_KEY")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    KAFKA_SERVERS = os.getenv("KAFKA_SERVERS", "localhost:9092")