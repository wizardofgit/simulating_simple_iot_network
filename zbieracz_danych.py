import json
from flask import Flask, request, render_template, redirect
import paho.mqtt.client as clt
import time

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    conf = [request.json['id'], 'HTTP', 'http://localhost:5000/add_reading/', 1, 'test.mosquitto.org', 'pwr/sensors', 1, 'austin_weather.csv', True] #id, method, url, interval, broker, topic, reading, source, on
    registered.append(conf)
    status_log.append((request.json['id'], time.time(), 'True', conf[3])) #id, last seen, on, interval
    registered.sort()
    status_log.sort()

    return 'Registration successful!'

@app.route('/deregister', methods=['POST'])
def deregister():
    for i in range(len(registered)):
        if registered[i][0] == request.json['id']:
            del registered[i]
            del status_log[i]
            registered.sort()
            status_log.sort()
            break
    return "Deregistration successful!"

@app.route('/add_reading/', methods=['POST'])
def add_http_reading():
    collected_raw_data.append(request.json)
    send_data = clt.Client()
    send_data.connect('test.mosquitto.org')
    send_data.publish('pwr/collected_data', json.dumps(request.json))
    return 'Record received'

@app.route('/config', methods=['GET'])
def config():
    for i in range(len(registered)):
        if registered[i][0] == request.json['id']:
            x = registered[i]
            conf = {'method': x[1], 'url': x[2], 'interval': x[3], 'broker': x[4], 'topic': x[5], 'reading': x[6], 'source': x[7], 'on': x[8]}
            status_log[i] = (status_log[i][0], time.time(), x[8], status_log[i][3])

            return conf

@app.route('/data')
def data():
    return collected_raw_data

@app.route('/status')
def status():
    s = "<html><body><h1>Status of the devices:</h1>"

    for i in status_log:
        if i[2] == 'False':
            s += f"Device id={i[0]} is stopped. <br>"
        elif int(time.time()) > (int(i[1]) + i[3] + 15):
            s += f"Device id={i[0]} is offline. Last seen: {time.ctime(i[1])}<br>"
        else:
            s+= f"Device id={i[0]} is online. <br>"

    s += "</body></head></html>"

    return s

@app.route('/device', methods=["POST", "GET"])
def select_device():
    if request.method == "POST":
        id = int(request.form['id'])
        return redirect(f'/config/{id}')
    else:
        return render_template('devices.html')

@app.route('/config/<int:id>', methods=["POST", "GET"]) #by zmienic config wchodzimy na /change_config?id=0 dla id=0
def change_config(id):
    if request.method == "POST":
        y = request.form
        x = registered[id]

        for i in range(len(y.keys())):
            if y[list(y.keys())[i]] != "":
                x[i+1] = y[list(y.keys())[i]]

        registered[id] = x

        return redirect(f'/changes_done?id={id}')
    else:
        return render_template('form.html', id=id)

@app.route('/changes_done', methods=['POST', 'GET'])
def changes_done():
    if request.method == 'POST':
        return redirect(request.form['url'])
    else:
        id = request.args['id']
        return render_template('changes.html', id=id)

@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == 'POST':
        return redirect(request.form['url'])
    else:
        return render_template('home.html')

@app.route('/registered')
def registered_devices():
    return registered

@app.route('/aggregate')
def aggregate():
    return redirect('http://localhost:1000/')

@app.route('/filter')
def filter():
    return redirect('http://localhost:2500/')

def on_message(client, userdata, message):
    collected_raw_data.append(json.loads(message.payload))
    send_data = clt.Client()
    send_data.connect('test.mosquitto.org')
    send_data.publish('pwr/collected_data', json.dumps(message.payload))

if __name__ == '__main__':
    collected_raw_data = [] #zbiór danych od czujników
    registered = []
    status_log = []

    client = clt.Client()   #ustawianie klienta MQTT
    client.connect('test.mosquitto.org')
    client.on_message = on_message
    client.loop_start()
    client.subscribe('pwr/sensors')

    app.run(debug=True, port=5000)  #odpalanie serwera