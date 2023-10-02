import json
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = '0c20320445392a19d9b2a02ae290502c'
BASE_URL = 'http://api.weatherstack.com/current'

def get_weather(city):
    params = {
        'access_key': API_KEY,
        'query': city,
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        temperature_celsius = data['current']['temperature']
        temperature_fahrenheit = (temperature_celsius * 9/5) + 32
        temperature_kelvin = temperature_celsius + 273.15
        description = data['current']['weather_descriptions'][0]
        country = data['location']['country']
        longitude = data['location']['lon']
        latitude = data['location']['lat']
        humidity = data['current']['humidity']
        
        # Additional data
        visibility = data['current']['visibility']
        wind_speed = data['current']['wind_speed']
        wind_direction = data['current']['wind_dir']
        atmospheric_pressure = data['current']['pressure']
        time_zone = data['location']['utc_offset']

        return {
            'city': city,
            'country': country,
            'temperature': temperature_celsius,
            'fahrenheit': temperature_fahrenheit,
            'kelvin': temperature_kelvin,
            'description': description,
            'longitude': longitude,
            'latitude': latitude,
            'humidity': humidity,
            'visibility': visibility,
            'wind_speed': wind_speed,
            'wind_direction': wind_direction,
            'atmospheric_pressure': atmospheric_pressure,
            'time_zone': time_zone,
        }
    except requests.exceptions.RequestException as e:
        status_code = e.response.status_code if e.response is not None else None
        error_message = 'Network error. Please check your internet connection and try again.'
        return {
            'error': f'Error {status_code}: {error_message}',
        }
    except (KeyError, ValueError) as e:
        status_code = 400
        error_message = 'Invalid data received from the server.'
        return {
            'error': f'Error {status_code}: {error_message}',
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None

    if request.method == 'POST':
        city = request.form.get('city')
        weather_data = get_weather(city)
        
        if 'error' in weather_data:
            error_message = weather_data['error']
        else:
            return render_template('index.html', **weather_data)
    
    return render_template('index.html', city='', country='', temperature='', description='', error=error_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(debug=True)