import subprocess
import itertools

# Define the parameters for the tests
producers = [1, 5, 10]
consumers = [1, 5, 10]
message_sizes = [1024, 1048575]  # 1 KB and 1 MB
topic = "perf-test"
num_records = [100000, 1000]  # Total messages to send/consume
throughput = [100000, 1000]  # Messages per second
broker = "localhost:9092"  # Kafka broker URI

def run_producer_test(producers, message_size, num_records, throughput):
    producer_command = [
        "bin/kafka-producer-perf-test.sh",
        f"--topic={topic}",
        f"--num-records={num_records}",
        f"--record-size={message_size}",
        f"--throughput={throughput}",
        "--producer-props", "bootstrap.servers=localhost:9092", "acks=all",
        "max.request.size=2097152"
    ]

    result = subprocess.run(producer_command,
    capture_output=True, text=True)

    if result.returncode == 0:
        print("Producer test completed successfully.")
        print(result.stdout)
    else:
        print("Producer test failed.")
        print(result.stderr)



def run_consumer_test(consumers, num_records):
    consumer_command = [
        "bin/kafka-consumer-perf-test.sh",
        f"--topic={topic}",
        f"--messages={num_records}",
        f"--broker-list={broker}",
        f"--group=test-consumer-group"
    ]

    print(f"Running consumer test with {consumers} consumers...")
    result = subprocess.run(consumer_command,
    capture_output=True, text=True)

    if result.returncode == 0:
        print("Consumer test completed successfully.")
        print(result.stdout)
    else:
        print("Consumer test failed.")
        print(result.stderr)

def run_scalability_tests():
    producer_counts = [10, 20, 30, 40, 50]
    consumer_counts = [10, 20, 30, 40, 50]

    for prod_count, cons_count, msg_size in itertools.product(producer_counts, consumer_counts, message_sizes):
        if msg_size == 1024:
            print(f"Testing scalability: {prod_count} producers, {cons_count} consumers, {msg_size}B message size.")
            run_producer_test(prod_count, msg_size, num_records[0], throughput[0])
            run_consumer_test(cons_count, num_records[0])
        else:
            print(f"Testing scalability: {prod_count} producers, {cons_count} consumers, {msg_size}B message size.")
            run_producer_test(prod_count, msg_size, num_records[1], throughput[1])
            run_consumer_test(cons_count, num_records[1])

run_scalability_tests()
