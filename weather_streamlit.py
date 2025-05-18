import requests

url = "https://easy-weather1.p.rapidapi.com/daily/5"

querystring = {"latitude":"1.28","longitude":"103.86"}

headers = {
	"x-rapidapi-key": "c0a6f42258mshcceedc1d343e8c8p161593jsnb5ed74fe152f",
	"x-rapidapi-host": "easy-weather1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

import requests
import pandas as pd

# Step 1: Make API request
url = "https://easy-weather1.p.rapidapi.com/daily/5"
querystring = {"latitude": "1.28", "longitude": "103.86"}
headers = {
    "x-rapidapi-key": "c0a6f42258mshcceedc1d343e8c8p161593jsnb5ed74fe152f",
    "x-rapidapi-host": "easy-weather1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

# Step 2: Extract 5-day forecast data
days = data['forecastDaily']['days']

# Step 3: Flatten all nested fields for each day
flat_data = []
for day in days:
    # Base level
    base = {k: v for k, v in day.items() if k not in ['daytimeForecast', 'overnightForecast']}
    # Nested daytime
    daytime = {f"daytime_{k}": v for k, v in day.get('daytimeForecast', {}).items()}
    # Nested overnight
    overnight = {f"overnight_{k}": v for k, v in day.get('overnightForecast', {}).items()}
    # Combine all
    flat_data.append({**base, **daytime, **overnight})

# Step 4: Convert to DataFrame
df = pd.DataFrame(flat_data)

# Step 5: Display or save
print(df)  # You’ll see all 5 rows

# Optional: Save to CSV
# df.to_csv("weather_forecast_singapore.csv", index=False)

df.head()
