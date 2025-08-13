import streamlit as st
import requests
import uuid

COHERE_API_KEY = st.secrets["COHERE_API_KEY"]

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

st.set_page_config(page_title="AI Mood Tracker", page_icon="🧠")
st.title("🧠 AI-Powered Mood Tracker")
st.markdown("Enter your thoughts below and the AI will classify your mood.")

user_text = st.text_area("How are you feeling today?", height=100)

if st.button("Analyze My Mood"):
    if not user_text.strip():
        st.error("⚠ Please enter some text before analyzing.")
    else:
        headers = {
            "Authorization": f"Bearer {COHERE_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "command-r",
            "messages": [
                {
                    "role": "user",
                    "content": f"Classify the following text into one of: Happy, Sad, Anxious, Angry, Neutral, Crisis.\nText: {user_text}\nOnly return the label."
                }
            ]
        }

        response = requests.post(
            "https://api.cohere.ai/v1/chat",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            try:
                # Cohere response structure for command-r chat:
                mood = response.json()["message"]["content"][0]["text"].strip()
                st.success(f"**Detected Mood:** {mood}")
            except Exception:
                st.error("Unexpected response format from Cohere.")
                st.write(response.json())
        else:
            st.error(f"❌ API Error: {response.text}")
