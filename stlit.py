import streamlit as st
import requests
import datetime
import uuid

COHERE_API_KEY = st.secrets["xLeVaX1IIBLGINcNuBI50LGDDlkZJdYoF5g2AnyO"]
COHERE_URL = "https://api.cohere.ai/v1/classify"

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

st.title("🧠 AI Mood Tracker")

user_text = st.text_area("How are you feeling today?", height=100)

if st.button("Analyze My Mood"):
    if not user_text.strip():
        st.error("Please enter some text.")
    else:
        headers = {
            "Authorization": f"Bearer {COHERE_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "embed-english-v3.0",
            "inputs": [user_text.strip()],
            "examples": [
                {"text": "I am feeling great today!", "label": "Happy"},
                {"text": "I feel terrible and lonely", "label": "Sad"},
                {"text": "I'm a bit stressed about work", "label": "Anxious"},
                {"text": "Everything is fine", "label": "Neutral"},
                {"text": "I'm so angry with them", "label": "Angry"}
            ]
        }
        response = requests.post(COHERE_URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            mood = data["classifications"][0]["prediction"]
            st.success(f"Mood: {mood}")
        else:
            st.error(f"Error: {response.text}")
