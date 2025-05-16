To run throughput and latency tests:
1. Run `bin/zookeeper-server-start.sh config/zookeeper.properties` command to start zookeper
2. Run `bin/kafka-server-start.sh config/server.properties` command to start kafka server
3. Run throughput-latency.py file.

To run scalability tests:
1. Run `bin/zookeeper-server-start.sh config/zookeeper.properties` command to start zookeper
2. Run `bin/kafka-server-start.sh config/server.properties` command to start kafka server
3. Run scalability.py file.

results_throughput.txt and results_scalability.txt files contain redacted script invocation results.