import streamlit as st
import requests
import uuid

# ----------------------------
# CONFIGURATION
# ----------------------------
COHERE_API_KEY = st.secrets.get("COHERE_API_KEY", None)

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

st.set_page_config(page_title="AI Mood Tracker", page_icon="🧠")
st.title("🧠 AI-Powered Mood Tracker")
st.markdown("Enter your thoughts below and the AI will classify your mood.")

# ----------------------------
# USER INPUT
# ----------------------------
user_text = st.text_area("How are you feeling today?", height=100)

# ----------------------------
# RULE-BASED BACKUP
# ----------------------------
def rule_based_mood(text):
    moods = {
        "Happy": ["happy", "great", "good", "joy", "excited", "glad"],
        "Sad": ["sad", "lonely", "unhappy", "depressed", "down"],
        "Anxious": ["anxious", "stressed", "nervous", "worried"],
        "Angry": ["angry", "mad", "frustrated", "irritated"],
        "Neutral": ["okay", "fine", "bored", "meh"]
    }
    text_lower = text.lower()
    for mood, keywords in moods.items():
        if any(word in text_lower for word in keywords):
            return mood
    return "Neutral"

# ----------------------------
# MOOD ANALYSIS
# ----------------------------
if st.button("Analyze Mood"):
    if not user_text.strip():
        st.error("⚠ Please enter some text before analyzing.")
    else:
        mood_detected = None

        # ---- Option 1: Cohere Generate ----
        if COHERE_API_KEY:
            try:
                headers = {
                    "Authorization": f"Bearer {COHERE_API_KEY}",
                    "Content-Type": "application/json"
                }
                prompt = f"""
Classify the following text into one of: Happy, Sad, Anxious, Angry, Neutral, Crisis.
Text: "{user_text}"
Return only the label.
"""
                payload = {
                    "model": "command-xlarge-nightly",
                    "prompt": prompt,
                    "max_tokens": 10
                }
                response = requests.post(
                    "https://api.cohere.ai/generate",
                    headers=headers,
                    json=payload,
                    timeout=10
                )
                if response.status_code == 200:
                    mood_detected = response.json()["generations"][0]["text"].strip()
                else:
                    st.warning("Cohere API failed, using rule-based mood detection.")
            except Exception as e:
                st.warning("Cohere API error, falling back to rule-based detection.")

        # ---- Option 2: Rule-Based ----
        if not mood_detected:
            mood_detected = rule_based_mood(user_text)

        st.success(f"**Detected Mood:** {mood_detected}")

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
st.caption("Powered by Cohere / Rule-Based Fallback • Privacy-Friendly • Made with ❤️ in Streamlit")
