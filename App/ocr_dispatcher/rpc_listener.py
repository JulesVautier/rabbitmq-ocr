#!/usr/bin/env python
import json
import os
from time import sleep

import pika
import threading

from .models import OcrResult


class ListenerRpc(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        self.task_response = self.channel.queue_declare('rpc_response_queue', durable=True)
        self.channel.basic_consume(self.on_response, queue=self.task_response.method.queue, no_ack=True)


    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)
        print('response : ',  self.response)
        ocr_result = OcrResult(result='hello hello hello', ocr_request_id=self.response['ocr_request_id'])
        ocr_result.save()

    def run(self):
        print(' [x] Waiting for responses from workers')
        self.channel.start_consuming()

