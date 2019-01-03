#!/usr/bin/env python
import json
import pika
import uuid


class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        self.task_queue = self.channel.queue_declare('rpc_task_queue')
        self.task_response = self.channel.queue_declare('rpc_response_queue')


    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.body = json.dumps({"number": n, "path": "/very/long/path", "type": "electricity"})
        self.channel.basic_publish(exchange='',
                                   routing_key=self.task_queue.method.queue,
                                   properties=pika.BasicProperties(
                                       reply_to=self.task_response.method.queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=str(self.body)
                                   )
        while self.response is None:
            self.connection.process_data_events()
        return self.response


fibonacci_rpc = FibonacciRpcClient()
fibonacci_rpc.call(30)