from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve
import threading
import time
import requests

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    # Check for empty strings or string with only spaces
    if not bool(city.strip()):
        # You could render "City Not Found" instead like we do below
        city = "Kansas City"

    weather_data = get_current_weather(city)

    # City is not found by API
    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')

    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )
    
def keep_alive():
    while True:
        try:
            requests.get('https://test-gnhu.onrender.com/')  # Replace with your actual app URL
            print("Ping sent!")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        time.sleep(600)  # Sleep for 10 minutes, adjust as needed

if __name__ == "__main__":
    # Start the background thread
    thread = threading.Thread(target=keep_alive)
    thread.daemon = True  # Allow thread to exit when the app exits
    thread.start()
    
    serve(app, host="0.0.0.0", port=8000)
