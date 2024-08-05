import paho.mqtt.client as mqtt
import time
import random
import threading

BROKER = "localhost"  # Replace with your broker's IP/hostname
PORT = 1883
TOPICS = ["test/topic1", "test/topic2", "test/topic3"]
QOS_LEVELS = [0, 1, 2]


# Simulate a client that subscribes to multiple topics
def subscriber_client(client_id):
    client = mqtt.Client(client_id)
    client.connect(BROKER, PORT, 60)

    def on_message(msg):
        print(f"{client_id} received message on {msg.topic}: {msg.payload.decode()}")

    client.on_message = on_message
    client.subscribe([(TOPICS[0], 0), (TOPICS[1], 1), (TOPICS[2], 2)])

    client.loop_start()
    time.sleep(15)
    client.loop_stop()


# Simulate a client that publishes to different topics with various QoS levels
def publisher_client(client_id):
    client = mqtt.Client(client_id)
    client.connect(BROKER, PORT, 60)

    client.loop_start()
    for _ in range(10):  # Adjust the range for more messages
        topic = random.choice(TOPICS)
        qos = random.choice(QOS_LEVELS)
        message = f"Message from {client_id} to {topic} with QoS {qos}"
        client.publish(topic, message, qos=qos)
        print(f"{client_id} published: {message}")
        time.sleep(random.uniform(0.5, 2.0))

    client.loop_stop()
    client.disconnect()


# Simulate clients that connect and disconnect frequently
def connect_disconnect_client(client_id):
    for _ in range(5):  # Adjust the range for more connect/disconnect cycles
        client = mqtt.Client(client_id)
        client.connect(BROKER, PORT, 60)
        print(f"{client_id} connected")
        time.sleep(random.uniform(1.0, 3.0))
        client.disconnect()
        print(f"{client_id} disconnected")
        time.sleep(random.uniform(1.0, 2.0))


# Run different scenarios in parallel using threads
if __name__ == "__main__":
    threads = []

    # Start subscriber clients
    for i in range(3):
        t = threading.Thread(target=subscriber_client, args=(f"subscriber-{i}",))
        threads.append(t)
        t.start()

    # Start publisher clients
    for i in range(3):
        t = threading.Thread(target=publisher_client, args=(f"publisher-{i}",))
        threads.append(t)
        t.start()

    # Start connect/disconnect clients
    for i in range(2):
        t = threading.Thread(target=connect_disconnect_client, args=(f"connect-disconnect-{i}",))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    print("All scenarios completed.")
