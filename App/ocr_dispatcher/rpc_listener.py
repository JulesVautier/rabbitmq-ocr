#!/usr/bin/env python
import json
import os
from time import sleep

import pika
import threading

from django.core import serializers

from .models import OcrResult, OcrResultSerializer


class ListenerRpc(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        self.task_response = self.channel.queue_declare('rpc_response_queue', durable=True)
        self.channel.basic_consume(self.on_response, queue=self.task_response.method.queue, no_ack=True)
        self.daemon = True

    def on_response(self, ch, method, props, body):
        body = json.loads(body.decode())
        serializer_ocr = OcrResultSerializer(data=body)
        if serializer_ocr.is_valid():
            OcrResult.objects.filter(pk=body['id']).update(status='DONE')

    def run(self):
        print(' [x] Waiting for responses from workers')
        self.channel.start_consuming()
