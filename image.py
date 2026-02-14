# streamlit_gemini_app.py

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import time
import traceback
from PIL import Image
import google.generativeai as genai


# -------------------------------------------------
# ✅ PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Leaf Image Recognizer", layout="centered")
st.title("🌿 Leaf Image Recognizer using Gemini AI")


# -------------------------------------------------
# ✅ LOAD API KEY
# -------------------------------------------------
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ GOOGLE_API_KEY is missing in your .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=API_KEY)


# -------------------------------------------------
# ✅ PROMPT TEMPLATE
# -------------------------------------------------
BASE_PROMPT = """
You are an expert in analyzing leaves.

You will be given an image of a leaf.

Your task is to:

1. Identify the leaf and its tree
2. Explain its health benefits
3. Describe its medical uses

Answer strictly in this format:

Identification:
- Scientific Name:
- Common Name:
- Tree Description:

Health Benefits:
- Medicinal Properties:
- Key Nutrients/Compounds:

Medical Uses:
- Traditional Uses:
- Modern Uses:
"""


# -------------------------------------------------
# ✅ GEMINI RESPONSE FUNCTION (WITH RETRY)
# -------------------------------------------------
def get_gemini_response(prompt_text, image, user_question):
    """
    Sends image + prompt to Gemini Vision Model
    Handles rate limit + quota errors properly
    """

    final_prompt = f"{prompt_text}\n\nUser Question: {user_question}"

    model = genai.GenerativeModel("gemini-2.0-flash")

    # Retry system (3 attempts)
    for attempt in range(3):
        try:
            response = model.generate_content([final_prompt, image])
            return response.text

        except Exception as e:

            # If quota exceeded → stop immediately
            if "429" in str(e) or "Quota exceeded" in str(e):
                return """
❌ Gemini API Quota Exceeded.

Your Google Cloud project currently has 0 requests/min enabled.

✅ Fix:
1. Enable Billing in Google Cloud
2. Enable Generative Language API
3. Request Quota Increase

Then try again.
"""

            # Retry after delay
            time.sleep(2)

    return "❌ Failed after multiple attempts. Please try again later."


# -------------------------------------------------
# ✅ USER INPUTS
# -------------------------------------------------
user_text = st.text_input("Enter your question (optional):")
uploaded_file = st.file_uploader("Upload a leaf image", type=["jpg", "jpeg", "png"])

image = None

if uploaded_file:
    try:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Leaf Image", use_container_width=True)

    except Exception as e:
        st.error("❌ Invalid image file.")
        st.stop()


# -------------------------------------------------
# ✅ SUBMIT BUTTON
# -------------------------------------------------
if st.button("🔍 Analyze Leaf"):

    if image is None:
        st.warning("⚠️ Please upload an image first.")
        st.stop()

    question = user_text.strip() or "Identify this leaf and explain its uses."

    with st.spinner("Gemini is analyzing the leaf... 🌱"):
        result = get_gemini_response(BASE_PROMPT, image, question)

    st.subheader("✅ Gemini Response")
    st.write(result)
