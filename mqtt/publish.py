import paho.mqtt.client as paho
import time


def publish(number):
  client = paho.Client(client_id="test", clean_session=False)
  # client.on_publish = on_publish
  client.connect('broker.mqttdashboard.com', 1883)
  client.loop_start()

  while True:
    msg = f"{number}"
    client.publish('openfind123', msg)
    time.sleep(1)

publish(84521)