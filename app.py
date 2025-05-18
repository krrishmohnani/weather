import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import base64

# Set background image
def set_background(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

#

# Apply custom font
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# Sample dataset
data = {
    'conditionCode': ['Drizzle', 'Rain', 'Rain', 'Drizzle', 'Drizzle'],
    'temperatureMax': [33.10, 29.75, 30.19, 31.02, 31.73],
    'temperatureMin': [28.03, 26.94, 26.73, 26.92, 26.90],
    'maxUvIndex': [9, 6, 7, 7, 8],
    'precipitationChance': [0.43, 0.84, 0.74, 0.65, 0.59]
}

# Load data into DataFrame
df = pd.DataFrame(data)

# Features and target
X = df[['conditionCode', 'temperatureMax', 'temperatureMin', 'maxUvIndex']]
y = df['precipitationChance']

# Preprocessing pipeline
categorical_features = ['conditionCode']
numeric_features = ['temperatureMax', 'temperatureMin', 'maxUvIndex']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('num', 'passthrough', numeric_features)
    ]
)

# Build and train the model
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

model.fit(X, y)

# Streamlit app
st.title("🌧️ Precipitation Chance Predictor")

# Input fields for a single record
st.subheader("Enter Weather Details")
condition_code = st.selectbox("Condition Code", ['Drizzle', 'Rain'])
temperature_max = st.number_input("Temperature Max (°C)", min_value=0.0, max_value=50.0, value=30.0)
temperature_min = st.number_input("Temperature Min (°C)", min_value=0.0, max_value=50.0, value=25.0)
max_uv_index = st.number_input("Max UV Index", min_value=0, max_value=10, value=7)

# Predict button
if st.button("Predict"):
    # Create DataFrame for the single input
    input_df = pd.DataFrame([{
        'conditionCode': condition_code,
        'temperatureMax': temperature_max,
        'temperatureMin': temperature_min,
        'maxUvIndex': max_uv_index
    }])

    # Predict precipitation chance
    prediction = model.predict(input_df)[0]

    # Display prediction
    st.subheader("Predicted Precipitation Chance")
    st.write(f"{prediction * 100:.2f}%")