#!/usr/bin/env python
import json

import pika
import uuid

class ListenerRpc(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()
        self.task_response = self.channel.queue_declare('rpc_response_queue')

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.task_response.method.queue)

    def on_response(self, ch, method, props, body):
        print("On listenner")
        self.response = body
        print('response : ',  self.response)

    def start(self):
        self.channel.start_consuming()


listener_rpc = ListenerRpc()
listener_rpc.start()

