import streamlit as st
from PIL import Image
import numpy as np
import time
from pose_analysis import analyze_pose
from feedback.voice import VoiceFeedback
import mediapipe as mp

# ---------------- STREAMLIT SETUP ----------------
st.set_page_config(page_title="Yoga Pose Coach", layout="wide")
st.title("🧘 YogAI — Real-Time Yoga Pose Detection")

# Pose selection
pose_name = st.selectbox("Select Pose:", ["tree", "tadasana", "namaste", "chair"])
feedback_interval = st.slider("Feedback Interval (seconds):", 1.0, 5.0, 2.5)

# Initialize voice feedback
voice = VoiceFeedback(cooldown=feedback_interval)

# Mediapipe setup
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose_model = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

st.write("📸 Capture your pose using the camera below:")

# Camera input (browser-friendly)
camera_input = st.camera_input("Capture Frame")

last_feedback_time = 0

if camera_input:
    # Convert uploaded frame to numpy array
    image = Image.open(camera_input)
    frame = np.array(image)
    h, w = frame.shape[:2]

    # Process with MediaPipe
    results = pose_model.process(frame)

    overlay_text = ""

    if results.pose_landmarks:
        # Draw landmarks
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
        )

        # Convert landmarks to dictionary
        landmarks = {
            idx: (int(lm.x * w), int(lm.y * h), lm.z, lm.visibility)
            for idx, lm in enumerate(results.pose_landmarks.landmark)
        }

        # Feedback logic with cooldown
        current_time = time.time()
        if current_time - last_feedback_time >= feedback_interval:
            issues = analyze_pose(landmarks, pose_name)
            if issues:
                overlay_text = "⚠️ " + ", ".join(issues)
                voice.speak(", ".join(issues))
            else:
                overlay_text = "✅ Good posture"
                voice.speak("Good posture, keep going")
            last_feedback_time = current_time

    # Overlay feedback text on frame
    if overlay_text:
        import cv2  # Only for putText
        color = (0, 0, 255) if "⚠️" in overlay_text else (0, 255, 0)
        cv2.putText(frame, overlay_text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, color, 2, cv2.LINE_AA)

    # Display frame in Streamlit
    st.image(frame, caption="Processed Frame", use_column_width=True)

st.write("✅ Session Ended. Thank you for practicing!")
