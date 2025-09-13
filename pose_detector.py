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

# Feedback interval
feedback_interval = st.slider("Feedback Interval (seconds):", 1.0, 5.0, 2.5)
voice = VoiceFeedback(cooldown=feedback_interval)

# Pose selection buttons
pose_name = st.radio("Select Yoga Pose:", ["tree", "tadasana", "namaste", "chair"])

# Mediapipe setup
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose_model = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

st.write("📸 Capture your pose using the camera below:")

# Camera input (browser-friendly)
camera_input = st.camera_input("Capture Frame")

last_feedback_time = 0

if camera_input:
    image = Image.open(camera_input)
    frame = np.array(image)
    h, w = frame.shape[:2]

    # Process frame
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

        # Convert to dict
        landmarks = {
            idx: (int(lm.x * w), int(lm.y * h), lm.z, lm.visibility)
            for idx, lm in enumerate(results.pose_landmarks.landmark)
        }

        # Feedback logic
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

    # Overlay text on frame
    if overlay_text:
        import cv2
        color = (0, 0, 255) if "⚠️" in overlay_text else (0, 255, 0)
        cv2.putText(frame, overlay_text, (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

    st.image(frame, caption=f"Pose: {pose_name}", use_column_width=True)

st.write("✅ Session Ended. Thank you for practicing!")
