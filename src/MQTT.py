from umqtt.robust import MQTTClient
from config import MQTT_CONFIG
import time

class MQTT:
    HOST = MQTT_CONFIG["host"]
    PORT = MQTT_CONFIG["port"]
    CLIENT_ID = MQTT_CONFIG["client_id"]

    def __init__(self):
        self.client = MQTTClient(client_id = self.CLIENT_ID, server = self.HOST, port = self.PORT)
        self.last_actuator_message = None

    def connect_mqtt(self):
        self.client.connect()
        print("MQTT Connected")
        return self.client

    def make_sensor_topic(self, sensor, data_type):
        return "i483/sensors/s2610115/{}/{}".format(sensor, data_type)

    def make_payload(self, value):
        return "{:.2f}".format(value)

    def publish_sensor_value(self, sensor, data_type, value):
        topic = self.make_sensor_topic(sensor, data_type)
        payload = self.make_payload(value)

        # print("Topic_{}_{} = {}".format(sensor, data_type, topic))
        # print("Payload_{}_{} = {}".format(sensor, data_type, payload))
        self.client.publish(topic, payload)

    def check_messages(self):
        self.client.check_msg()

    def on_message(self, topic, msg):
        print(f"Receive msg from MQTT. Topic: {topic}, Payload: {msg}")
        #print("topic =", topic)
        #print("payload =", msg)
        self.last_actuator_message = msg

    def check_messages(self):
        self.client.check_msg()

