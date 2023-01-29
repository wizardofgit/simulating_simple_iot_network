from flask import Flask, request, render_template, redirect
import paho.mqtt.client as clt
import json
from datetime import datetime

app = Flask(__name__)

filters = {'reading': '', 'start': '', 'stop': '', 'over': '', 'under': ''}

@app.route('/', methods=['POST', 'GET'])
def filtering():
    if request.method == 'POST':
        params = request.form
        for key in params:
            if key != '':
                filters[key] = params[key]

        return redirect('http://localhost:5000/')
    else:
        return render_template('filter.html')

def on_message(client, userdata, message):
    data = json.loads(message.payload)
    format = '%Y-%m-%d'
    send_data = clt.Client()
    send_data.connect('test.mosquitto.org')
    ifs_to_satisfy = 0
    ifs_satisfied = 0
    date_data = datetime.strptime(data['date'], format)

    for key in filters:
        if filters[key] != '':
            ifs_to_satisfy += 1

    if filters['start'] != '':
        date_start = datetime.strptime(filters['start'], format)
        if date_start >= date_data:
            ifs_satisfied += 1
    if filters['start'] != '':
        date_stop = datetime.strptime(filters['stop'], format)
        if date_stop <= date_data:
            ifs_satisfied += 1
    if filters['reading'] != '':
        if data['reading_name'] == filters['reading']:
            ifs_satisfied += 1
    if filters['over'] != '':
        if int(data['reading']) > int(filters['over']):
            ifs_satisfied += 1
    if filters['under'] != '':
        if int(data['reading']) < int(filters['under']):
            ifs_satisfied += 1

    if ifs_satisfied == ifs_to_satisfy:
        send_data.publish('pwr/filtered_data', json.dumps(data))


if __name__ == '__main__':
    client = clt.Client()
    client.connect('test.mosquitto.org')
    client.subscribe('pwr/collected_data')
    client.on_message = on_message
    client.loop_start()

    app.run(debug=True, port=2500)  #odpalanie serwera
