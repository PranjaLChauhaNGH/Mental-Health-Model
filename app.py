import streamlit as st
import requests

# Configure the Streamlit page
st.set_page_config(page_title="Mental Health Predictor", layout="centered")

# Set the URL for your FastAPI backend
FASTAPI_URL = "https://mental-health-model-db6p.onrender.com/predict"

st.title("Mental Health Prediction Model")
st.markdown("Enter the user metrics below to send a prediction request to the FastAPI backend.")

# Build the form for user inputs
with st.form("prediction_form"):
    st.header("User Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Age constraints updated to match ge=10, le=90
        age = st.number_input("Age", min_value=10, max_value=90, value=20, step=1)
        gender = st.selectbox("Gender", ["Male", "Female"])
        academic_level = st.selectbox("Academic Level", ["Undergraduate", "Graduate", "High School"])
        country = st.selectbox("Country", [
            "Australia", "Canada", "France", "Germany", "India", 
            "Mexico", "Turkey", "UK", "USA", "Other"
        ])
        
    with col2:
        study_hours = st.number_input("Study Hours (Daily)", min_value=0.0, max_value=24.0, value=4.0, step=0.5)
        sleep_hours = st.number_input("Sleep Hours Per Night", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
        physical_activity = st.number_input("Physical Activity Hours", min_value=0.0, max_value=24.0, value=1.0, step=0.5)
        stress_level = st.selectbox("Stress Level", ["Medium", "Low", "High", "Very High"])
        
    st.header("Device & Usage Metrics")
    col3, col4 = st.columns(2)
    
    with col3:
        avg_daily_usage = st.number_input("Avg Daily Usage Hours", min_value=0.0, max_value=24.0, value=5.0, step=0.5)
        daily_unlocks = st.number_input("Daily Unlocks", min_value=0, max_value=500, value=50, step=1)
        
    with col4:
        most_used_platform = st.selectbox("Most Used Platform", [
            "Facebook", "LinkedIn", "Instagram", "Snapchat", "Twitter",
            "YouTube", "TikTok", "LINE", "KakaoTalk", "VKontakte", "WhatsApp",
            "WeChat"
        ])
        purpose_of_use = st.selectbox("Purpose Of Use", ["Networking", "Education", "Entertainment", "News"])

    # Form submit button
    submit_button = st.form_submit_button("Predict Mental Health Score")

# Handle the API request when the user clicks submit
if submit_button:
    # Construct the JSON payload with exact casing matching the StudentData BaseModel
    payload = {
        "age": age,
        "gender": gender,
        "country": country,
        "academic_level": academic_level,
        "most_used_platform": most_used_platform,
        "purpose_of_use": purpose_of_use,
        "avg_daily_usage_hours": avg_daily_usage,
        "daily_unlocks": daily_unlocks,
        "study_hours": study_hours,
        "physical_activity_hours": physical_activity,
        "sleep_hours_per_night": sleep_hours,
        "stress_level": stress_level
    }
    
    try:
        with st.spinner("Connecting to FastAPI backend..."):
            response = requests.post(FASTAPI_URL, json=payload)
            
        # Parse and display the response
        if response.status_code == 200:
            result = response.json()
            # Adjust 'prediction' based on the actual key returned by your FastAPI backend
            prediction_value = result.get("predicted_mental_health_score", result)
            st.success(f"### Predicted Result: {prediction_value}")
        else:
            st.error(f"Error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Failed to connect to the backend. Ensure your FastAPI server is running locally on port 8000.")
