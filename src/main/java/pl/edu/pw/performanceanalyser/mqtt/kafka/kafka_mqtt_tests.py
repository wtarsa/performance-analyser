import paho.mqtt.client as mqtt
from pykafka import KafkaClient
import time
import threading
import random
import string

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'kafka_mqtt'

NUM_PRODUCERS = [1, 5, 10]
NUM_CONSUMERS = [1, 5, 10]
NUM_PRODUCERS_SCALABILITY = [10, 20, 30, 40, 50]
NUM_CONSUMERS_SCALABILITY = [10, 20, 30, 40, 50]
MSG_SIZES = {"1KB": 1024, "1MB": 1024 * 1024}
MSG_COUNTS = {"1KB": 4000, "1MB": 200}

def generate_message(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

class MQTTProducer(threading.Thread):
    def __init__(self, msg_size, msg_count):
        super().__init__(daemon=True)
        self.msg_size = msg_size
        self.msg_count = msg_count
        self.client = mqtt.Client()
        self.client.connect(MQTT_BROKER, MQTT_PORT)

    def run(self):
        for _ in range(self.msg_count):
            message = generate_message(self.msg_size)
            self.client.publish(KAFKA_TOPIC, message)
        self.client.disconnect()

class KafkaConsumer(threading.Thread):
    def __init__(self, msg_count, start_time):
        super().__init__(daemon=True)
        self.client = KafkaClient(hosts=KAFKA_BROKER)
        self.topic = self.client.topics[KAFKA_TOPIC]
        self.consumer = self.topic.get_simple_consumer()
        self.msg_count = msg_count
        self.start_time = start_time
        self.received_times = []

    def run(self):
        received = 0
        for message in self.consumer:
            if message is not None:
                receive_time = time.time()
                latency = receive_time - self.start_time
                self.received_times.append(latency)
                received += 1
                if received >= self.msg_count:
                    break
        avg_latency = sum(self.received_times) / len(self.received_times) if self.received_times else 0
        print(f'Average latency: {avg_latency:.4f} seconds')

class MQTTBridge(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.client = mqtt.Client()
        self.client.connect(MQTT_BROKER, MQTT_PORT)
        self.kafka_client = KafkaClient(hosts=KAFKA_BROKER)
        self.kafka_topic = self.kafka_client.topics[KAFKA_TOPIC]
        self.kafka_producer = self.kafka_topic.get_producer()

    def on_message(self, client, userdata, message):
        msg_payload = message.payload.decode()
        self.kafka_producer.produce(msg_payload.encode('ascii'))

    def run(self):
        self.client.subscribe(KAFKA_TOPIC)
        self.client.on_message = self.on_message
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.kafka_producer.stop()

def run_tests():
    for num_producers in NUM_PRODUCERS:
        for num_consumers in NUM_CONSUMERS:
            for size_label, msg_size in MSG_SIZES.items():
                msg_count = MSG_COUNTS[size_label]
                print(f'Testing {num_producers} producers, {num_consumers} consumers, message size: {size_label}')

                bridge = MQTTBridge()
                bridge.start()

                start_time = time.time()
                consumers = [KafkaConsumer(msg_count, start_time) for _ in range(num_consumers)]
                for c in consumers:
                    c.start()

                producers = [MQTTProducer(msg_size, msg_count) for _ in range(num_producers)]
                for p in producers:
                    p.start()

                for p in producers:
                    p.join()
                end_time = time.time()

                total_time = end_time - start_time
                msg_per_sec = (num_producers * msg_count) / total_time if total_time > 0 else 0
                print(f'Finished in {total_time:.2f} seconds, Messages per second: {msg_per_sec:.2f}')

                for c in consumers:
                    c.join()
                bridge.stop()
                time.sleep(1)

def run_scalability_tests():
    for num_producers in NUM_PRODUCERS_SCALABILITY:
        for num_consumers in NUM_CONSUMERS_SCALABILITY:
            for size_label, msg_size in MSG_SIZES.items():
                msg_count = MSG_COUNTS[size_label]
                print(f'Testing {num_producers} producers, {num_consumers} consumers, message size: {size_label}')

                bridge = MQTTBridge()
                bridge.start()

                start_time = time.time()
                consumers = [KafkaConsumer(msg_count, start_time) for _ in range(num_consumers)]
                for c in consumers:
                    c.start()

                producers = [MQTTProducer(msg_size, msg_count) for _ in range(num_producers)]
                for p in producers:
                    p.start()

                for p in producers:
                    p.join()
                end_time = time.time()

                total_time = end_time - start_time
                msg_per_sec = (num_producers * msg_count) / total_time if total_time > 0 else 0
                print(f'Finished in {total_time:.2f} seconds, Messages per second: {msg_per_sec:.2f}')

                for c in consumers:
                    c.join()
                bridge.stop()
                time.sleep(1)

if __name__ == '__main__':
    run_tests()
    run_scalability_tests()
