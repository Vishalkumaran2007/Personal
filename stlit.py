import streamlit as st
import requests
import datetime
import uuid

# ---------- CONFIG ----------
N8N_WEBHOOK_URL = "https://vishal1234.app.n8n.cloud/webhook/eda2512c-bc29-480e-9124-e0c8c6cbdc0b"  # Replace with your n8n webhook URL

# Generate or retrieve a persistent user_id
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

st.set_page_config(page_title="AI Mood Tracker", page_icon="🧠", layout="centered")

st.title("🧠 AI-Powered Mood Tracker")
st.write("Check your mood, get supportive feedback, and track trends.")

# ---------- USER INPUT ----------
st.subheader("💬 How are you feeling today?")
user_text = st.text_area(
    "Type your feelings here:",
    height=100,
    placeholder="I feel anxious about work deadlines..."
)

# ---------- SUBMIT ----------
if st.button("Analyze My Mood"):
    if not user_text.strip():
        st.error("Please write how you are feeling before submitting.")
    else:
        payload = {
            "user_id": st.session_state.user_id,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "message": user_text.strip()
        }
        
        try:
            response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                mood = data.get("mood", "Unknown")
                support_message = data.get("support_message", "")
                
                st.success(f"**Mood Detected:** {mood}")
                st.write(f"💡 *{support_message}*")
            else:
                st.error(f"Error from n8n: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")

# ---------- WEEKLY SUMMARY ----------
st.subheader("📊 Weekly Mood Summary")
if st.button("Load Weekly Report"):
    try:
        summary_url = f"{N8N_WEBHOOK_URL}-summary"  # Example: separate webhook for weekly summary
        summary_resp = requests.get(summary_url, params={"user_id": st.session_state.user_id})
        if summary_resp.status_code == 200:
            content = summary_resp.json()
            if "chart_base64" in content:
                import base64
                chart_bytes = base64.b64decode(content["chart_base64"])
                st.image(chart_bytes, caption="Your Weekly Mood Trend")
            else:
                st.info("No summary chart available yet.")
        else:
            st.error(f"Error: {summary_resp.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
