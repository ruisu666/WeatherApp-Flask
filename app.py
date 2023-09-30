import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace 'YOUR_API_KEY' with your actual Weatherstack API key
API_KEY = '0c20320445392a19d9b2a02ae290502c'
BASE_URL = 'http://api.weatherstack.com/current'

def get_weather(city):
    params = {
        'access_key': API_KEY,
        'query': city,
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        temperature = data['current']['temperature']
        description = data['current']['weather_descriptions'][0]
        return {
            'city': city,
            'temperature': temperature,
            'description': description,
            'weather_image': get_weather_image(description.lower())
        }
    else:
        return None

# Define temperature ranges and corresponding image filenames
temperature_images = {
    'cold': 'cold.png',           # Temperature less than 10°C
    'mild': 'mild.png',           # Temperature between 10°C and 20°C
    'warm': 'warm.png',           # Temperature between 20°C and 30°C
    'hot': 'hot.png',             # Temperature greater than or equal to 30°C
    'default': 'default.png',     # Default image for unknown temperature ranges
}

def get_weather_image(temperature):
    # Determine the temperature range and select the corresponding image
    if temperature < 10:
        return temperature_images['cold']
    elif 10 <= temperature < 20:
        return temperature_images['mild']
    elif 20 <= temperature < 30:
        return temperature_images['warm']
    elif temperature >= 30:
        return temperature_images['hot']
    else:
        return temperature_images['default']

# Modify the get_weather function to get the temperature
def get_weather(city):
    params = {
        'access_key': API_KEY,
        'query': city,
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        temperature = data['current']['temperature']
        description = data['current']['weather_descriptions'][0]
        return {
            'city': city,
            'temperature': temperature,
            'description': description,
            'weather_image': get_weather_image(temperature)  # Use temperature to get the image
        }
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form.get('city')
        weather_data = get_weather(city)
        if weather_data:
            return render_template('index.html', **weather_data)
        else:
            return "Unable to fetch weather data for the provided city."
    return render_template('index.html', city='', temperature='', description='', weather_image='default.png')

if __name__ == '__main__':
    app.run(debug=True)
