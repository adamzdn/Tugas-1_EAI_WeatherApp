import streamlit as st
import requests

st.markdown(
    '''
    <style>
    .stApp,.e8zbici2 {
    background-image: url("https://wallpaperaccess.com/full/2417426.jpg");
    background-size: cover;
    }
    .reportview-container {
    background: url("https://wallpaperaccess.com/full/2417426.jpg")
    }
    </style>
    ''',
    unsafe_allow_html=True
)

def get_weather(city):
    """Fetches weather data for a given city using the OpenWeatherMap API.

    Args:
        city: The name of the city to get weather data for.

    Returns:
        A dictionary containing weather data for the given city, or None if an error occurs.
    """
    url = f"https://open-weather13.p.rapidapi.com/city/{city}"
    headers = {
        "X-RapidAPI-Key": "4a80c78b51msh2461f8321028bd4p1ce5bajsndba52f9c189e",  # Replace with your actual API key
        "X-RapidAPI-Host": "open-weather13.p.rapidapi.com",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching weather data: {e}")
        return None

def get_five_day_forecast(lat, lon):
    """Fetches five-day forecast data for a given latitude and longitude.

    Args:
        lat: The latitude of the location.
        lon: The longitude of the location.

    Returns:
        A dictionary containing five-day forecast data, or None if an error occurs.
    """
    url = f"https://open-weather13.p.rapidapi.com/city/fivedaysforcast/{lat}/{lon}"
    headers = {
        "X-RapidAPI-Key": "4a80c78b51msh2461f8321028bd4p1ce5bajsndba52f9c189e",  # Replace with your actual API key
        "X-RapidAPI-Host": "open-weather13.p.rapidapi.com",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching five-day forecast data: {e}")
        return None

st.title("Weather App")

city = st.text_input("Enter city name:")

if st.button("Get Weather"):
    weather_data = get_weather(city)
    if weather_data:
        icon = weather_data['weather'][0]['icon']
        temp_fahrenheit = weather_data['main']['temp']
        temp_celsius = (temp_fahrenheit - 32) * 5.0/9.0
        st.header(f"**{weather_data['name']}**")
        st.image(f"https://openweathermap.org/img/wn/{icon}@2x.png")
        st.subheader(f"{temp_celsius:.2f} °C")        
        st.write(f"**Weather:** {weather_data['weather'][0]['main']}")
        st.write(f"**Description:** {weather_data['weather'][0]['description']}") 
        

        # Get and display five-day forecast (optional)
        if weather_data.get('coord'):  # Check if coordinates are available
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']
            forecast_data = get_five_day_forecast(lat, lon)
            if forecast_data:
                st.subheader("Five-Day Temperature Average")
                daily_temperatures = {}  # Dictionary to store daily temperatures
                for day in forecast_data['list']:  # Loop through each entry in the forecast
                    date = day['dt_txt'][:10]  # Extract date from datetime string
                    temp_kelvin = day['main']['temp']  # Get temperature in Kelvin
                    temp_celsius = temp_kelvin - 273.15  # Convert Kelvin to Celsius
                    weather = day['weather'][0]['main']  # Get weather condition
                    # Aggregate temperatures for each day
                    if date not in daily_temperatures:
                        daily_temperatures[date] = []
                    daily_temperatures[date].append(temp_celsius)
                # Calculate average temperature for each day and display
                for date, temps in daily_temperatures.items():
                    avg_temp = sum(temps) / len(temps)
                    st.write(f"{date}: Average Temperature: {avg_temp:.2f} °C")

    else:
        st.warning("An error occurred while fetching weather data.")
