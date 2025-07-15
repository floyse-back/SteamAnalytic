import json

import pika

from app.domain.logger import ILogger


class EventProducer:
    def __init__(self,logger: ILogger):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.logger = logger

    def send_message(self,body:dict,queue:str):
        self.channel.queue_declare(queue=queue,auto_delete=True)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(body,default=str),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )
        self.logger.info("[x] Sent Message")

    def close(self):
        self.connection.close()