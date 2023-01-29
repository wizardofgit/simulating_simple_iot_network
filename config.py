import json

def default_config():
    config = {
        'method': ('HTTP', 'HTTP', 'HTTP', 'HTTP', 'HTTP'),
        'url': ('http://localhost:5000/add_reading/', 'http://localhost:5000/add_reading/',
                'http://localhost:5000/add_reading/', 'http://localhost:5000/add_reading/',
                'http://localhost:5000/add_reading/'),
        'interval': (1, 1, 1, 1, 1),
        'broker': (
        'test.mosquitto.org', 'test.mosquitto.org', 'test.mosquitto.org', 'test.mosquitto.org', 'test.mosquitto.org'),
        'topic': ('pwr/sensor/', 'pwr/sensor/', 'pwr/sensor/', 'pwr/sensor/', 'pwr/sensor/'),
        'reading': (1, 2, 3, 8, 20),
        'source': (
        'austin_weather.csv', 'austin_weather.csv', 'austin_weather.csv', 'austin_weather.csv', 'austin_weather.csv')
    }

    with open('default_config.json', 'w') as f:
        f.write(json.dumps(config, indent=len(config.keys())))

#default_config()
