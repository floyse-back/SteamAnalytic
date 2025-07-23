import json

import pika

from app.domain.logger import ILogger
from app.utils.config import RABBITMQ_HOST

class Consumer:
    def __init__(self,logger:ILogger):
        self.connection = None
        self.channel = None
        self.logger = logger

    def connect(self):
        self.logger.info("Connecting to rabbitmq")
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(f"{RABBITMQ_HOST}"))
        self.channel = self.connection.channel()

    def consume(self):
        if self.channel is None:
            self.connect()

        self.channel.queue_declare(queue="sub_appids", durable=True)

        def callback(ch, method, properties, body):
            self.logger.info("Get:%s", body.decode())
            from app.infrastructure.celery_app.tasks.subscribes_tasks import update_wishlist_batches
            data = json.loads(body.decode())
            update_wishlist_batches.delay(data)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue="sub_appids",on_message_callback=callback)
        self.logger.info("Consume message")
        self.channel.start_consuming()

