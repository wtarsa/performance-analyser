To run tests:
1. Run `bin/zookeeper-server-start.sh config/zookeeper.properties` command to start zookeper
2. Run `bin/kafka-server-start.sh config/server.properties` command to start kafka server
3. Install mosquitto broker and run `mosquitto -v` command to start broker
4. Run `bin/kafka-topics.sh --create --topic kafka_mqtt --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1` to create kafka_mqtt topic
5. Run `python3 kafka_mqtt_tests.py`
