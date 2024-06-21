from confluent_kafka import Producer
import json
import time

p = Producer({'bootstrap.servers': 'localhost:29092'})


def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def send_order(order):
    data = json.dumps(order)
    p.produce(topic='orders', value=data.encode('utf-8'), callback=delivery_report)
    p.flush()


if __name__ == "__main__":
    i = 1
    while True:
        order = {"order": i}
        send_order(order)
        i += 1
        time.sleep(1)
