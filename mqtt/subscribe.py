import paho.mqtt.client as paho
import reactivex as rx
from reactivex import operators as ops

def on_subscribe(client, userdata, mid, granted_qos):
  print("Subscribed: "+str(mid)+" "+str(granted_qos))

# def on_message(client, userdata, msg):
#   # print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
#   data.next({
#     "topic": msg.topic,
#     "qos": msg.qos,
#     "payload": msg.payload
#   })

def on_disconnect(client, userdata, rc):
  logging.info("disconnecting reason  "  +str(rc))
  client.connected_flag=False
  client.disconnect_flag=True

def subscribe(on_message, on_subscribe=on_subscribe, on_disconnect=on_subscribe):
  client = paho.Client()
  client.on_subscribe = on_subscribe
  client.on_message = on_message
  client.on_disconnect = on_disconnect
  client.connect('broker.mqttdashboard.com', 1883)
  client.subscribe('openfind123')
  client.loop_start()
