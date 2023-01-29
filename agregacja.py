from flask import Flask, request, render_template, redirect
from statistics import mean, median
import paho.mqtt.client as clt
import json

app = Flask(__name__)

buffer = []

@app.route('/', methods=['POST', 'GET'])
def aggregate():
    if request.method == 'POST':
        params = request.form
        answer = ""

        if params['mean'] == 'yes':
            answer += f"Mean of the data: {mean(buffer[-10:])}<br>"
        if params['median'] == 'yes':
            answer += f"Median of the data: {median(buffer[-10:])}<br>"

        return answer
    else:
        return render_template('aggregation.html')

@app.route('/buffer')
def show_buffer():
    return buffer

def on_message(client, userdata, message):
    buffer.append(int(json.loads(message.payload)['reading']))

    if len(buffer) > 20:
        del buffer[10:]
    #print(json.loads(message.payload))

if __name__ == '__main__':
    client = clt.Client()
    client.connect('test.mosquitto.org')
    client.subscribe('pwr/filtered_data')
    client.on_message = on_message
    client.loop_start()

    app.run(debug=True, port=1000)  #odpalanie serwera

