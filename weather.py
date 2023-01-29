import time
import csv
import paho.mqtt.client as clt
import requests
import json

class Weather_sensor():
    def __init__(self, sensor_number):
        self.sensor_number = sensor_number
        self.reading_name = ""
        self.register()
        self.config()

    def config(self):
        r = requests.get('http://localhost:5000/config', json={'id': self.sensor_number})
        config = r.json()

        self.source = config['source']
        self.url = config['url']
        self.method = config['method']
        self.interval = config['interval']
        self.broker = config['broker']
        self.topic = config['topic']
        self.reading = config['reading']
        self.on = config['on']

    def register(self):
        conf = {'id' : self.sensor_number}
        r = requests.post('http://localhost:5000/register', json=conf)

    def deregister(self):
        conf = {'id': self.sensor_number}
        r = requests.post('http://localhost:5000/deregister', json=conf)

    def collect_data(self):
        with open(self.source, 'r') as f:
            aw = csv.reader(f)
            header = next(aw)
            self.reading_name = header[self.reading]
            aw = list(aw)
            config_counter = 0

        while True:
            for i in range(len(aw)):
                line = aw[i]
                if config_counter == 2:
                    config_counter = 0
                    self.config()

                if self.on == 'False':
                    print("Device stopped")
                    time.sleep(self.interval)
                    config_counter += 1
                elif self.method == 'HTTP':
                    r = requests.post(self.url, json={'sensor': self.sensor_number,'date': line[0], 'reading_name': self.reading_name ,'reading': line[self.reading], 'method': self.method})
                    print(f'Record sent from sensor {self.sensor_number} using {self.method}')
                    time.sleep(self.interval)
                    config_counter += 1
                else:
                    client = clt.Client()
                    client.connect(self.broker)
                    client.loop_start()

                    client.publish(self.topic, json.dumps({'sensor': self.sensor_number,'date': line[0], 'reading_name': self.reading_name ,'reading': line[self.reading], 'method': self.method}))
                    print(f'Record sent from sensor {self.sensor_number} using {self.method}')
                    time.sleep(self.interval)
                    config_counter += 1
