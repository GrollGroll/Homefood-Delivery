import json
import logging

from confluent_kafka import Producer

logging.basicConfig(level=logging.INFO
                    )
p = Producer({'bootstrap.servers': 'localhost:29092'})


def delivery_report(err, msg):
    if err is not None:
        logging.INFO('Message delivery failed: {}'.format(err))
    else:
        logging.INFO('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def send_order_data(user, order_data):
    data = {'user': user, 'order': order_data}
    data = json.dumps(data)
    p.produce(topic='orders_data', value=data.encode('utf-8'), callback=delivery_report)
    p.flush()
