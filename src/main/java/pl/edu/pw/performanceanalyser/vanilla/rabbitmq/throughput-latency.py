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

# Run tests for all combinations of parameters
for prod, cons, msg_size, queue_pat in itertools.product(producers, consumers, message_sizes, queue_patterns):
    run_test(prod, cons, msg_size, queue_pat)
