#!/usr/bin/env python
import json

import pika
import time

QUEUE = 'rpc_task_queue'

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue=QUEUE)

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def on_request(ch, method, props, body):
    print('before:', body)
    body = json.loads(body)
    n = int(body['number'])

    print(" [.] fib(%s)" % n)
    body['number'] = fib(n)
    time.sleep(3)
    print ('slept')

    response = body

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print('finished')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue=QUEUE)

print(" [x] Awaiting RPC requests")
channel.start_consuming()