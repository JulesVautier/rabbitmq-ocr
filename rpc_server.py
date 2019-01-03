#!/usr/bin/env python
import json

import pika
import time


class WorkerRpc(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()
        self.task_queue = self.channel.queue_declare(queue='rpc_task_queue', durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.on_request, queue=self.task_queue.method.queue)


    def compute(self, n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.compute(n - 1) + self.compute(n - 2)


    def on_request(self, ch, method, props, body):
        print('recieved : ', body)
        body = json.loads(body)
        n = int(body['number'])
        body['number'] = self.compute(n)
        response = body

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id,
                             delivery_mode=2),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print('finished')


    def start(self):
        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()

workder_rpc = WorkerRpc()
workder_rpc.start()