import json

import pika

from app.infrastructure.logger.logger import logger
from app.utils.config import RABBITMQ_HOST


class Consumer:
    def __init__(self):
        self.connection = None
        self.channel = None

    def connect(self):
        logger.info("Connecting to rabbitmq")
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(f"{RABBITMQ_HOST}"))
        self.channel = self.connection.channel()

    def consume(self):
        if self.channel is None:
            self.connect()

        self.channel.queue_declare(queue="sub_appids", durable=True)

        def callback(ch,method,properties,body):
            logger.info("Get:%s", body.decode())
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue="sub_appids",on_message_callback=callback)
        logger.info("Consume message")
        self.channel.start_consuming()

