from confluent_kafka import Producer

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()}')

producer = Producer({'bootstrap.servers': 'localhost:9092'})

producer.produce('my_topic', key='key', value='fetch_data', callback=delivery_report)
producer.flush()
