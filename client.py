import json

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("zigbee2mqtt/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    print(str(msg.payload))
    payload = json.loads(str(msg.payload.decode('UTF-8')))
    endpoint = 0
    if msg.topic == "zigbee2mqtt/ovladac_satna":
        endpoint = 2
    elif msg.topic == "zigbee2mqtt/ovladac_pracovna" or msg.topic == "zigbee2mqtt/ovladac_pracovna_2":
        endpoint = 1

    if "action" in payload:
        if payload["action"] == "on":
            # switch ON
            publish.single('zigbee2mqtt/spinac_pracovna/set', '{"state_right":"ON"}',
                           hostname="localhost")
        elif payload["action"] == "off":
            # switch off
            publish.single('zigbee2mqtt/spinac_pracovna/set', '{"state_right":"OFF"}',
                           hostname="localhost")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
# Add message callbacks that will only trigger on a specific subscription match.
#client.message_callback_add("zigbee2mqtt/ovladac_pracovna_2/", on_message)
#client.message_callback_add("zigbee2mqtt/ovladac_pracovna/", on_message)
client.message_callback_add("zigbee2mqtt/ovladac_satna/", on_message)
# client.message_callback_add("$SYS/broker/bytes/#", on_message_bytes)
# client.on_message = on_message
client.connect("localhost", 1883, 60)
#client.subscribe("zigbee2mqtt/ovladac_pracovna_2", 0)
#client.subscribe("zigbee2mqtt/ovladac_pracovna", 0)
client.subscribe("zigbee2mqtt/ovladac_satna", 0)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
