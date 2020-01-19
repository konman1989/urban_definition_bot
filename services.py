import json
import pika


def init_json_creation(dict_):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='127.0.0.1'
    ))
    channel = connection.channel()

    channel.queue_declare(queue=json.dumps(dict_))

    channel.basic_publish(
        exchange='',
        routing_key='dict_',
        body=json.dumps(dict_),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )
