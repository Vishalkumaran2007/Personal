import streamlit as st
import requests
import uuid

# ----------------------------
# CONFIGURATION
# ----------------------------
# Store your Cohere API key in .streamlit/secrets.toml like:
# COHERE_API_KEY = "your_api_key_here"
COHERE_API_KEY = st.secrets["COHERE_API_KEY"]

# Generate a unique session ID for each user
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# ----------------------------
# STREAMLIT UI
# ----------------------------
st.set_page_config(page_title="AI Mood Tracker", page_icon="🧠")
st.title("🧠 AI-Powered Mood Tracker")
st.markdown("Enter your thoughts below and the AI will classify your mood.")

# Text input
user_text = st.text_area("How are you feeling today?", height=100)

# ----------------------------
# MOOD ANALYSIS
# ----------------------------
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

        # Send request to Cohere Chat API
        response = requests.post(
            "https://api.cohere.ai/v1/chat",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            try:
                mood = response.json()["message"]["content"][0]["text"].strip()
                st.success(f"**Detected Mood:** {mood}")
            except Exception as e:
                st.error("Unexpected response format from Cohere.")
                st.write(response.json())
        else:
            st.error(f"❌ API Error: {response.text}")

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
st.caption("Powered by Cohere • Privacy-Friendly • Made with ❤️ in Streamlit")
