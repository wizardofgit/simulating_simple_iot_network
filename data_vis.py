import time
from matplotlib import pyplot as plt
import paho.mqtt.client as clt
import json
import numpy as np

data_filtered = []
data_unfiltered = []

def on_message1(client, userdata, message):
    data_filtered.append(float(json.loads(message.payload.decode('utf-8'))["reading"]))

def on_message2(client, userdata, message):
    data_unfiltered.append(float(json.loads(message.payload.decode('utf-8'))["reading"]))

def visualize(list):
    if len(list) == 0:
        print('No data to show')
        return
    print(list)
    plt.plot(range(1,len(list) + 1), list)
    plt.show()

client1 = clt.Client('data_filtered')
client1.connect('test.mosquitto.org')
client1.subscribe('pwr/filtered_data')
client1.on_message = on_message1
client2 = clt.Client('data_aggregated')
client2.connect('test.mosquitto.org')
client2.subscribe('pwr/collected_data')
client2.on_message = on_message2
client1.loop_start()
client2.loop_start()

while True:
    if input() == 'f':
        visualize(data_filtered)
    else:
        visualize(data_unfiltered)