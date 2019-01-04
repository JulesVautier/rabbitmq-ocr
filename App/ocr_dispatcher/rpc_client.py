#!/usr/bin/env python
import json
import pika
import uuid

from django.core import serializers

from .models import OcrResult

class ClientRpc(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        self.task_queue = self.channel.queue_declare('rpc_task_queue', durable=True)
        self.task_response = self.channel.queue_declare('rpc_response_queue', durable=True)

    def call(self, ocr_request: int, file: str):
        self.corr_id = str(uuid.uuid4())
        ocr_result = OcrResult(ocr_request_id=ocr_request, file_id=file)
        data = json.dumps(ocr_result)
        self.body = data
        print(self.body)
        self.channel.basic_publish(exchange='',
                                   routing_key=self.task_queue.method.queue,
                                   properties=pika.BasicProperties(
                                       reply_to=self.task_response.method.queue,
                                       correlation_id=self.corr_id,
                                       delivery_mode=2
                                   ),
                                   body=str(self.body)
                                   )


