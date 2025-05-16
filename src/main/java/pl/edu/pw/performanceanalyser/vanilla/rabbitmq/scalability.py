import subprocess
import itertools

# Define the parameters for the tests
producers = [1, 5, 10]
consumers = [1, 5, 10]
message_sizes = [1024, 1048576]  # 1 KB and 1 MB
queue_patterns = ["perf-test-%d"]
duration = 10  # seconds
uri = "amqp://localhost"

def run_test(producers, consumers, message_size, queue_pattern):
    command = [
        "java", "-jar", "perf-test-2.22.1.jar",
        f"--uri={uri}",
        f"--producers={producers}",
        f"--consumers={consumers}",
        f"--queue-pattern={queue_pattern}",
        "--queue-pattern-from=1",
        "--queue-pattern-to=1",
        f"--time={duration}",
        f"--size={message_size}"
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        print("Test completed successfully.")
        print(result.stdout)
    else:
        print("Test failed.")
        print(result.stderr)

def run_scalability_test(max_producers,
max_consumers, message_size, step=1):
    for producers in range(10, max_producers + 1, step):
        for consumers in range(10, max_consumers + 1, step):
            queue_pattern = f"perf-test-{producers}-{consumers}"
            run_test(producers, consumers, message_size, queue_pattern)

print("\n[STARTING SCALABILITY TEST]")
run_scalability_test(50, 50, message_size=1024, step=10)
run_scalability_test(50, 50, message_size=1048576, step=10)
