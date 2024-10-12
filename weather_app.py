import requests

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
        
        # Display the weather information
        print(f"Weather in {city}:")
        print(f"Description: {weather}")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
    else:
        print(f"Failed to retrieve weather data for {city}. HTTP Status code: {response.status_code}")

if __name__ == "__main__":
    # Replace with your OpenWeatherMap API key
    API_KEY = 'your_api_key_here'
    
    # City for which you want to get the weather
    city = input("Enter the city name: ")
    
    # Call the function to get weather data
    get_weather(city, API_KEY)
