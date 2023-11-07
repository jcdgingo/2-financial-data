from confluent_kafka import Consumer, KafkaError
import pandas as pd
import MetaTrader5 as mt5

def fetch_data():
    # Your code here, returning a DataFrame
    return pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my_group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['my_topic'])

while True:
    msg = consumer.poll(1)
    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break
    
    command = msg.value().decode('utf-8')
    if command == 'fetch_data':
        df = fetch_data()
        print(df)

consumer.close()
