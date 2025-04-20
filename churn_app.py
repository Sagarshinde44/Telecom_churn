import streamlit as st
import pandas as pd
from joblib import load
from sklearn.preprocessing import LabelEncoder

# Load model
model = load('random_forest_model.joblib')

# App Configuration
st.set_page_config(page_title="Customer Churn Predictor", page_icon="🔍", layout="centered")

# Add background graphics via CSS
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://www.transparenttextures.com/patterns/symphony.png"), 
                          linear-gradient(to right, #e0eafc, #cfdef3);
        background-size: auto, cover;
        background-repeat: repeat, no-repeat;
        background-attachment: fixed;
    }

    .css-18e3th9 {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    }

    #MainMenu, footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🔍 Customer Churn Prediction App</h1>", unsafe_allow_html=True)
st.markdown("---")

# Input Form
st.subheader("📋 Enter Customer Details")

col1, col2 = st.columns(2)
with col1:
    tenure = st.number_input("🕓 Tenure (months)", min_value=0, max_value=100, value=1, step=1)
    internet_service = st.selectbox("🌐 Internet Service", ('DSL', 'Fiber optic', 'No'))

with col2:
    contract = st.selectbox("📄 Contract Type", ('Month-to-month', 'One year', 'Two year'))
    monthly_charges = st.number_input("💵 Monthly Charges", min_value=0, max_value=200, value=50)
    total_charges = st.number_input("💰 Total Charges", min_value=0, max_value=10000, value=0)

# Radio to trigger prediction
st.markdown("---")
trigger = st.radio("🔮 Click to Predict", options=["🔮 Predict Churn"], index=0)

if trigger == "🔮 Predict Churn":
    # Label Mapping
    label_mapping = {
        'DSL': 0,
        'Fiber optic': 1,
        'No': 2,
        'Month-to-month': 0,
        'One year': 1,
        'Two year': 2,
    }
    internet_service = label_mapping[internet_service]
    contract = label_mapping[contract]

    # Prediction
    input_features = [[tenure, internet_service, contract, monthly_charges, total_charges]]
    prediction = model.predict(input_features)

    # Result
    st.markdown("---")
    st.subheader("🔎 Prediction Result")

    if prediction[0] == 0:
        st.success("✅ This customer is likely to stay.")
        st.balloons()
    else:
        st.error("⚠️ This customer is likely to churn.")
        st.markdown(
            "<p style='color: red;'>Consider retention strategies like better offers or personalized support.</p>",
            unsafe_allow_html=True
        )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 0.9em; color: gray;'>Built with ❤️ using Streamlit</div>",
    unsafe_allow_html=True
)
