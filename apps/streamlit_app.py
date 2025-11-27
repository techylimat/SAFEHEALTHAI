import streamlit as st
from ultralytics import YOLO
import numpy as np
from PIL import Image
import pandas as pd
import os
from dotenv import load_dotenv
import requests  # NEW: Library for making HTTP requests to the webhook

# --- CONFIGURATION & SETUP ---
load_dotenv()  # Load environment variables including ALERT_WEBHOOK_URL

# IMPORTANT: Update this path to your actual best model weights
MODEL_PATH = 'C:/Users/USER/PycharmProjects/PythonProject1/runs/detect/safehealth_model4/weights/best.pt'
ALERT_WEBHOOK_URL = os.getenv("ALERT_WEBHOOK_URL")  # Get the secret URL

st.set_page_config(
    page_title="SafeHealth AI",
    layout="centered",
    initial_sidebar_state="expanded"
)


# --- WEBHOOK AUTOMATION FUNCTION ---

def trigger_webhook(detection_summary: str, image_name: str, hazards: set) -> bool:
    """
    Sends a POST request to the configured Webhook URL when hazards are detected.
    This triggers the external no-code automation platform (Zapier/IFTTT).
    """
    if not ALERT_WEBHOOK_URL:
        st.warning("ALERT_WEBHOOK_URL missing from environment. Automated alert is disabled.")
        return False

    # Data payload sent to the webhook (Zapier/IFTTT)
    payload = {
        "file_name": image_name,
        "hazard_count": len(hazards),
        "detected_classes": list(hazards),
        "detection_summary_table": detection_summary,
        "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        # Send the POST request to the Webhook
        response = requests.post(ALERT_WEBHOOK_URL, json=payload, timeout=15)

        if response.status_code == 200 or response.status_code == 201:
            return True
        else:
            st.error(f"Webhook failed! Status code: {response.status_code}. Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to webhook URL. Check URL or internet connection. Error: {e}")
        return False


# --- CACHING THE MODEL (Crucial for Speed) ---
@st.cache_resource
def load_yolo_model(path):
    """Loads the model only once to prevent slow reloading on every interaction."""
    return YOLO(path)


model = load_yolo_model(MODEL_PATH)
CLASS_NAMES = model.names

# --- SIDEBAR AND PARAMETERS ---
st.sidebar.header("⚙️ Model Settings")
confidence_threshold = st.sidebar.slider(
    "Select Confidence Threshold (Higher = Fewer False Alarms)", 0.0, 1.0, 0.45, 0.05
)
st.sidebar.markdown(f"**Loaded Weights:** `{MODEL_PATH.split('/')[-1]}`")

# --- MAIN APP LAYOUT ---
st.title("🛡️ SafeHealth AI – Environmental Hazard Detection")
st.markdown("### 🔬 Analyze Images for Environmental Risks")
st.info(
    "Upload an image to detect stagnant water, trash hotspots, or blocked drainage. Alerts are sent via automated Webhook.")
st.markdown("---")

# File uploader
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)

    col_empty1, col_image, col_empty2 = st.columns([1, 3, 1])

    with col_image:
        st.subheader("Original Image")
        st.image(image, caption=uploaded_file.name, use_container_width=True)

    img = np.array(image)

    # --- BUTTON TO INITIATE DETECTION ---
    if st.button("🚀 Start Hazard Analysis"):
        st.markdown("---")

        with st.spinner(f"Analyzing image with a minimum confidence of **{confidence_threshold}**..."):
            # Perform object detection
            results = model.predict(img, conf=confidence_threshold)

            result_img = results[0].plot()

            with col_image:
                st.subheader("Hazard Detections")
                st.image(result_img, caption="Detections highlighted in the image.", use_container_width=True)

            st.markdown("---")

            # --- PROCESS DETECTIONS AND GENERATE ALERT ---
            detected_classes = set()
            boxes_data = []

            if results[0].boxes:
                boxes_data = results[0].boxes.data.cpu().numpy()
                for box in results[0].boxes:
                    cls_id = int(box.cls[0])
                    detected_classes.add(CLASS_NAMES[cls_id])

            if detected_classes:
                # --- PANDAS DATA FRAME CREATION ---
                df = pd.DataFrame(boxes_data,
                                  columns=['x_min', 'y_min', 'x_max', 'y_max', 'Confidence', 'Class_ID'])
                df['Class Name'] = df['Class_ID'].apply(lambda x: CLASS_NAMES[int(x)])
                df_display = df[['Class Name', 'Confidence', 'x_min', 'y_min', 'x_max', 'y_max']].sort_values(
                    by='Confidence', ascending=False)

                # --- UI ALERT AND RECOMMENDATION ---
                st.error("⚠️ **CRITICAL HAZARD ALERT: Immediate Action Required**")

                alert_map = {
                    "Stagnant water": "Potential breeding ground for mosquitoes and diseases.",
                    "Trash": "Risk of pollution, pests, and fire hazards.",
                    "Blocked drain": "Risk of flooding and infrastructural damage."
                }

                st.subheader("Assessment & Recommendations")
                for cls in detected_classes:
                    message = alert_map.get(cls, "Unidentified hazard detected.")
                    st.markdown(f"- **{cls}**: {message}")
                st.markdown("*Recommendation: Notify relevant municipal authorities for swift cleanup and mitigation.*")

                # --- WEBHOOK AUTOMATION TRIGGER ---
                with st.spinner("Sending automated alert via Webhook..."):
                    # Use only the relevant columns for the email summary table
                    summary_df = df_display[['Class Name', 'Confidence', 'x_min', 'y_min', 'x_max', 'y_max']]
                    summary_string = summary_df.to_markdown(index=False)

                    # Call the new webhook function
                    success = trigger_webhook(summary_string, uploaded_file.name, detected_classes)

                    if success:
                        st.success(
                            "✅ **Alert Sent!** Notification successfully dispatched to the response team via Webhook.")

                # --- RAW DATA DISPLAY ---
                with st.expander("📊 View Raw Detection Data (Scores & Coordinates)"):
                    st.dataframe(df_display, use_container_width=True)

            else:
                st.success("✅ **No identified hazards detected** at the selected confidence threshold.")