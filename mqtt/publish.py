import paho.mqtt.client as paho
import time, json

client = paho.Client(client_id="test", clean_session=False)

def publish(data):
  global client
  # client.on_publish = on_publish
  client.connect('broker.mqttdashboard.com', 1883)
  client.loop_start()

  while True:
    msg = json.dumps({"count": data})
    client.publish('openfind123', msg)
    time.sleep(1)