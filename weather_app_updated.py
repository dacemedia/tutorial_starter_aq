from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

def get_weather(city, api_key):
    # OpenWeatherMap API endpoint
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    # Make the request and get the response
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        
        # Extract weather data from the JSON response
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        
        # Return weather information as JSON
        return {
            "city": city,
            "description": weather,
            "temperature": temperature,
            "humidity": humidity
        }
    else:
        return {"error": f"Failed to retrieve weather data for {city}. HTTP Status code: {response.status_code}"}

@app.route('/weather', methods=['GET'])
def weather():
    # Extract the city from the request arguments
    city = request.args.get('city')
    
    # Replace with your OpenWeatherMap API key
    api_key = 'bdbf1eb7ad6358b6ebfb8104164e4b2d'
    
    # Get weather data
    weather_data = get_weather(city, api_key)
    
    # Return the weather data as a JSON response
    return jsonify(weather_data)

if __name__ == "__main__":
    app.run(debug=True)
