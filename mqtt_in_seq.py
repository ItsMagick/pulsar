import paho.mqtt.client as mqtt
import time
import random

BROKER = "127.0.0.1"
PORT = 1883
TOPICS = ["test/topic1", "test/topic2", "test/topic3", "invalid/topic"]
QOS_LEVELS = [0, 1, 2]
RUN_TIME = 2 * 60


def subscriber_client(client_id):
    client = mqtt.Client(client_id)
    client.connect(BROKER, PORT, 60)

    def on_message(msg):
        print(f"{client_id} received message on {msg.topic}: {msg.payload.decode()}")

    client.on_message = on_message
    client.subscribe([(TOPICS[0], 0), (TOPICS[1], 1), (TOPICS[2], 2)])

    client.loop_start()
    time.sleep(RUN_TIME)
    client.loop_stop()
    client.disconnect()


def publisher_client(client_id):
    client = mqtt.Client(client_id)
    client.connect(BROKER, PORT, 60)

    client.loop_start()
    start_time = time.time()
    while time.time() - start_time < RUN_TIME:
        topic = random.choice(TOPICS[:-1])
        qos = random.choice(QOS_LEVELS)
        message = f"Message from {client_id} to {topic} with QoS {qos}"
        client.publish(topic, message, qos=qos)
        print(f"{client_id} published: {message}")
        time.sleep(random.uniform(0.5, 2.0))

    client.loop_stop()
    client.disconnect()


def retained_message_client(client_id):
    client = mqtt.Client(client_id)
    client.connect(BROKER, PORT, 60)

    client.loop_start()
    start_time = time.time()
    while time.time() - start_time < RUN_TIME:
        for topic in TOPICS[:-1]:
            message = f"Retained message from {client_id} to {topic}"
            client.publish(topic, message, qos=0, retain=True)
            print(f"{client_id} published retained: {message}")
            time.sleep(random.uniform(2.0, 5.0))

    client.loop_stop()
    client.disconnect()


def will_message_client(client_id):
    client = mqtt.Client(client_id)
    client.will_set(TOPICS[0], payload=f"Will message from {client_id}", qos=1, retain=True)
    client.connect(BROKER, PORT, 60)

    client.loop_start()
    start_time = time.time()
    while time.time() - start_time < RUN_TIME:
        print(f"{client_id} connected and will set")
        time.sleep(random.uniform(1.0, 3.0))
        client.loop_stop()
        client.disconnect()
        print(f"{client_id} disconnected")
        time.sleep(random.uniform(1.0, 2.0))
        client.loop_start()

    client.disconnect()


def connect_disconnect_client(client_id):
    start_time = time.time()
    while time.time() - start_time < RUN_TIME:
        client = mqtt.Client(client_id)
        client.connect(BROKER, PORT, 60)
        print(f"{client_id} connected")
        time.sleep(random.uniform(1.0, 3.0))
        client.disconnect()
        print(f"{client_id} disconnected")
        time.sleep(random.uniform(1.0, 2.0))


def large_payload_client(client_id):
    client = mqtt.Client(client_id)
    client.connect(BROKER, PORT, 60)

    client.loop_start()
    start_time = time.time()
    while time.time() - start_time < RUN_TIME:
        large_message = "A" * 1024 * 64
        topic = random.choice(TOPICS[:-1])
        client.publish(topic, large_message, qos=1)
        print(f"{client_id} published large payload to {topic}")
        time.sleep(random.uniform(2.0, 5.0))

    client.loop_stop()
    client.disconnect()


def error_condition_client(client_id):
    client = mqtt.Client(client_id)
    client.connect(BROKER, PORT, 60)

    client.loop_start()
    start_time = time.time()
    while time.time() - start_time < RUN_TIME:
        try:
            client.publish(TOPICS[-1], "Invalid topic", qos=1)
            print(f"{client_id} published to invalid topic")
        except Exception as e:
            print(f"Error in {client_id} publishing: {e}")

        try:
            client.publish(TOPICS[0], "Invalid QoS", qos=3)
        except Exception as e:
            print(f"Error in {client_id} publishing with invalid QoS: {e}")

        time.sleep(random.uniform(1.0, 3.0))

    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":
    subscriber_client("subscriber-1")
    publisher_client("publisher-1")
    retained_message_client("retained-publisher")
    will_message_client("will-publisher")
    connect_disconnect_client("connect-disconnect-1")
    large_payload_client("large-payload-publisher")
    error_condition_client("error-client")

    print("All scenarios completed.")
