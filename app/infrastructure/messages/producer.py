import json
import pika

from app.infrastructure.logger.logger import logger


class EventProducer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

    def send_message(self,body:dict,queue:str):
        self.channel.queue_declare(queue=queue,auto_delete=True)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )
        logger.info("[x] Sent Message")

    def close(self):
        self.connection.close()