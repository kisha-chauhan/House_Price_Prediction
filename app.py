import streamlit as st
import pandas as pd
import pickle

# Load model and columns
model = pickle.load(open("model/model.pkl", "rb"))
columns = pickle.load(open("model/columns.pkl", "rb"))

# Page config
st.set_page_config(page_title="House Price Predictor", page_icon="🏠", layout="centered")

# Header
st.markdown("<h1 style='text-align: center;'>🏠 House Price Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>Predict property price based on features</p>", unsafe_allow_html=True)

st.image("https://images.unsplash.com/photo-1568605114967-8130f3a36994")

st.write("---")

# Layout (2 columns)
col1, col2 = st.columns(2)

with col1:
    area = st.number_input("📐 Area (sq ft)", min_value=0)
    bedrooms = st.number_input("🛏 Bedrooms", min_value=0)
    bathrooms = st.number_input("🛁 Bathrooms", min_value=0)

with col2:
    garage = st.number_input("🚗 Garage Capacity", min_value=0)
    basement = st.number_input("🏠 Basement Area", min_value=0)
    year = st.number_input("📅 Year Built", min_value=0)

# Location mapping
location_map = {
    "Luxury Area 💎": "CollgCr",
    "Standard Area 🏠": "Edwards",
    "Affordable Area 💰": "NAmes",
    "Old Developed Area 🏚️": "OldTown"
}

selected_location = st.selectbox("📍 Select Area Type", list(location_map.keys()))
location = location_map[selected_location]

st.write("")

# Predict Button Centered
if st.button("💰 Predict Price"):

    # Validation
    if area == 0 or bedrooms == 0 or bathrooms == 0 or year == 0:
        st.error("❌ Please enter all required details!")
    else:
        # Input Data
        input_data = pd.DataFrame([[area, bedrooms, bathrooms, garage, basement, year]],
                                 columns=['GrLivArea', 'BedroomAbvGr', 'FullBath',
                                          'GarageCars', 'TotalBsmtSF', 'YearBuilt'])

        # Add missing columns
        for col in columns:
            if col not in input_data.columns:
                input_data[col] = 0

        # Set location
        loc_col = "Neighborhood_" + location
        if loc_col in input_data.columns:
            input_data[loc_col] = 1

        # Fix column order
        input_data = input_data[columns]

        # Prediction
        prediction = model.predict(input_data)

        # Output box
        st.success(f"🏷 Estimated Price: ₹ {prediction[0]:,.2f}")

        # st.balloons()