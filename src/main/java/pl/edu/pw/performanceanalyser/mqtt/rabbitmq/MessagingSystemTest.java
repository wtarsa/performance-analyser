package pl.edu.pw.performanceanalyser.mqtt.rabbitmq;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class MessagingSystemTest {

    private static final int[] MESSAGE_SIZES = {1024, 1024 * 1024}; // 1 KB, 1 MB
    private static final int[] PRODUCER_COUNTS = {1, 5, 10};
    private static final int[] CONSUMER_COUNTS = {1, 5, 10};
    private static final int[] MESSAGE_COUNT = {500, 50};
    private static final int MAX_PRODUCERS = 50;
    private static final int MAX_CONSUMERS = 50;
    private static final int STEP_SIZE = 10;

    public static void main(String[] args) throws Exception {
        for (int producerCount : PRODUCER_COUNTS) {
            for (int consumerCount : CONSUMER_COUNTS) {
                for (int messageSize : MESSAGE_SIZES) {
                    System.out.println("Running test for RabbitMQ with " + producerCount + " producers, " + consumerCount +
                            " consumers, " + messageSize + " byte message size");

                        measureThroughput(producerCount, consumerCount, messageSize);
                        measureLatency(producerCount, consumerCount, messageSize);
                    }
                }
            measureScalability(10, 10, 1024);
            measureScalability(10, 10, 1048576);
        }
    }


    private static void measureThroughput(int producerCount, int consumerCount, int messageSize) {
        List<Producer> producers = new ArrayList<>();
        List<Consumer> consumers = new ArrayList<>();
        int messageCount = messageSize == 1024 ? MESSAGE_COUNT[0] : MESSAGE_COUNT[1];

        try {
            // Initialize producers and consumers
            for (int i = 0; i < producerCount; i++) {
                producers.add(new Producer());
            }
            for (int i = 0; i < consumerCount; i++) {
                consumers.add(new Consumer());
            }

            long startTime = System.currentTimeMillis();

            // Start producer threads
            ExecutorService executor = Executors.newFixedThreadPool(producerCount);
            for (Producer producer : producers) {
                executor.submit(() -> {
                    try {
                        for (int i = 0; i < messageCount; i++) {
                            producer.sendMessage(generateMessage(messageSize));
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                });
            }
            executor.shutdown();
            executor.awaitTermination(1, TimeUnit.HOURS);

            // Simulate consumers processing messages
            for (Consumer consumer : consumers) {
                consumer.waitForMessages();
            }

            long elapsedTime = System.currentTimeMillis() - startTime;
            System.out.println("Throughput: " + (producerCount * messageCount / (elapsedTime / 1000.0)) + " messages/sec");

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            // Clean up
            try {
                for (Producer producer : producers) {
                    producer.close();
                }
                for (Consumer consumer : consumers) {
                    consumer.close();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }


    private static void measureLatency(int producerCount, int consumerCount, int messageSize) throws Exception {
        Producer producer = createProducer();
        Consumer consumer = createConsumer();

        long startTime = System.nanoTime();
        producer.sendMessage(generateMessage(messageSize));
        consumer.waitForMessages();
        long elapsedTime = System.nanoTime() - startTime;

        System.out.println("Latency: " + elapsedTime + " ns");
    }

    private static void measureScalability(int initialProducers, int initialConsumers, int messageSize) {
        System.out.println("Testing scalability for " + messageSize + " byte message size");

        for (int producers = initialProducers; producers <= MAX_PRODUCERS; producers += STEP_SIZE) {
            for (int consumers = initialConsumers; consumers <= MAX_CONSUMERS; consumers += STEP_SIZE) {
                System.out.println("Testing with " + producers + " producers and " + consumers + " consumers.");
                measureThroughput(producers, consumers, messageSize);
            }
        }
    }

    private static Producer createProducer() throws Exception {
        return new Producer();
    }

    private static Consumer createConsumer() throws Exception {
        return new Consumer();
    }

    private static String generateMessage(int size) {
        return "X".repeat(size);
    }
}

