'''
MQTT
=============



'''

import time
import paho.mqtt.client as mqtt

broker="foo.com"

def on_message():
    time.sleep(1);
    print("received message =",str(message.payload.decode("utf-8")))


client= mqtt.Client("client-001")

client.on_message=on_message

print("CONNECT TO BROKER ", broker)
client.connect(broker)
client.loop_start()

print("SUBSCRIBE")
client.subscribe("foo/foo")
time.sleep(3)



client.disconnect()
client.loop_stop()

