package pl.edu.pw.performanceanalyser.mqtt.rabbitmq;

import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class Consumer {

    private final static String BROKER_URL = "tcp://localhost:1883"; // MQTT broker URL
    private final static String TOPIC = "perftest";

    private MqttClient client;

    public Consumer() throws MqttException {
        String clientId = MqttClient.generateClientId();
        client = new MqttClient(BROKER_URL, clientId, new MemoryPersistence());

        client.setCallback(new MqttCallback() {
            @Override
            public void connectionLost(Throwable cause) {
                System.out.println("Connection lost! Cause: " + cause.getMessage());
            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                String payload = new String(message.getPayload());
                System.out.println(" [x] Received message on topic '" + topic + "': " + payload);
                System.out.println(" [x] Received message size: " + payload.length());
            }

            @Override
            public void deliveryComplete(org.eclipse.paho.client.mqttv3.IMqttDeliveryToken token) {
                System.out.println("Delivery complete");
            }
        });

        // Connect to the broker
        MqttConnectOptions connOpts = new MqttConnectOptions();
        connOpts.setCleanSession(true);
        connOpts.setUserName("admin");
        connOpts.setPassword(new char[]{'a', 'd', 'm', 'i', 'n'});
        client.connect(connOpts);
        System.out.println("Connected to MQTT broker at " + BROKER_URL);
    }

    public void waitForMessages() {
        try {
            // Subscribe to the topic
            client.subscribe(TOPIC);
            System.out.println(" [*] Subscribed to topic: " + TOPIC);
        } catch (MqttException e) {
            System.out.println("Failed to subscribe to topic. Error: " + e.getMessage());
        }
    }

    public void close() {
        try {
            if (client.isConnected()) {
                client.disconnect();
            }
            client.close();
        } catch (MqttException e) {
            System.out.println("Failed to close MQTT client. Error: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        try {
            Consumer consumer = new Consumer();
            consumer.waitForMessages();

            // Keep the program running to receive messages
            Thread.sleep(10000); // Adjust as needed for your test
            consumer.close();
        } catch (MqttException | InterruptedException e) {
            System.out.println("Error initializing consumer: " + e.getMessage());
        }
    }
}
