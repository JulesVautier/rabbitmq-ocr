#!/usr/bin/env python
import io
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


    def compute(self, request):
        request['result'] = 'worked on worker heh'
        return request


    def on_request(self, ch, method, props, body):
        print(body)
        body = body.decode()
        print(body)
        request = json.loads(body)
        response = json.dumps(self.compute(request))
        print(response)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id,
                             delivery_mode=2),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)


    def start(self):
        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()

workder_rpc = WorkerRpc()
workder_rpc.start()