package pl.edu.pw.performanceanalyser.mqtt.rabbitmq;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.MqttException;

public class Producer {

    private final static String BROKER_URL = "tcp://localhost:1883"; // MQTT broker URL
    private final static String TOPIC = "perftest";

    private MqttClient client;

    public Producer() throws MqttException {
        String clientId = MqttClient.generateClientId();
        client = new MqttClient(BROKER_URL, clientId);

        MqttConnectOptions connOpts = new MqttConnectOptions();
        connOpts.setCleanSession(true);
        connOpts.setUserName("admin");
        connOpts.setPassword(new char[]{'a', 'd', 'm', 'i', 'n'});
        client.connect(connOpts);
    }

    public void sendMessage(String message) {
        try {
            MqttMessage mqttMessage = new MqttMessage(message.getBytes());
            mqttMessage.setQos(1);

            client.publish(TOPIC, mqttMessage);

            System.out.println(" [x] Sent '" + message + "' to topic '" + TOPIC + "'");
        } catch (MqttException e) {
            System.out.println("Failed to send message. Error: " + e.getMessage());
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
            Producer producer = new Producer();
            producer.sendMessage("Hello, MQTT!");
            producer.close();
        } catch (MqttException e) {
            System.out.println("Error initializing producer: " + e.getMessage());
        }
    }
}

