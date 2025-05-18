import streamlit as st
import requests
import pandas as pd

st.title("🌤️ 5-Day Weather Forecast")
st.markdown("Get a 5-day weather forecast by entering a location's coordinates.")

# Input fields
latitude = st.text_input("Enter Latitude:", value="1.28")
longitude = st.text_input("Enter Longitude:", value="103.86")

# Function to call API and get weather data
def get_weather_data(lat, lon):
    url = "https://easy-weather1.p.rapidapi.com/daily/5"
    querystring = {"latitude": lat, "longitude": lon}
    headers = {
        "x-rapidapi-key":"c0a6f42258mshcceedc1d343e8c8p161593jsnb5ed74fe152f" ,  # Replace with your actual key
        "x-rapidapi-host": "easy-weather1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    
    days = data['forecastDaily']['days']
    flat_data = []
    for day in days:
        base = {k: v for k, v in day.items() if k not in ['daytimeForecast', 'overnightForecast']}
        daytime = {f"daytime_{k}": v for k, v in day.get('daytimeForecast', {}).items()}
        overnight = {f"overnight_{k}": v for k, v in day.get('overnightForecast', {}).items()}
        flat_data.append({**base, **daytime, **overnight})
    
    return pd.DataFrame(flat_data)

# Button to trigger forecast
if st.button("Get Forecast"):
    if latitude and longitude:
        with st.spinner("Fetching data..."):
            try:
                df = get_weather_data(latitude, longitude)
                st.success("Forecast retrieved successfully!")
                st.dataframe(df)

                # Option to download
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("Download CSV", csv, "weather_forecast.csv", "text/csv")
            except Exception as e:
                st.error(f"Failed to retrieve data: {e}")
    else:
        st.warning("Please enter both latitude and longitude.")

