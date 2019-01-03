#!/usr/bin/env python
import json

import pika
import uuid

class ListenerRpc(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        self.task_response = self.channel.queue_declare('rpc_response_queue', durable=True)
        self.channel.basic_consume(self.on_response, queue=self.task_response.method.queue, no_ack=True)

    def on_response(self, ch, method, props, body):
        self.response = body
        print('response : ',  self.response)

    def start(self):
        print(' [x] Waiting for responses from workers')
        self.channel.start_consuming()


listener_rpc = ListenerRpc()
listener_rpc.start()

