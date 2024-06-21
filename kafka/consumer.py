from confluent_kafka import Consumer, KafkaException
import json

c = Consumer({
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['orders'])


def consume_orders():
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        order = json.loads(msg.value().decode('utf-8'))
        process_order(order)


def process_order(order):
    print(f"Processing order: {order}")


if __name__ == "__main__":
    consume_orders()
