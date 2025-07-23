from app.infrastructure.logger.logger import Logger
from app.infrastructure.messages.consumer import Consumer


def run_consumer():
    logger = Logger(name="infrastructure.rabbitmq", file_path="infrastructure")
    consumer = Consumer(logger=logger)
    logger.info("Consumer process started")
    consumer.consume()