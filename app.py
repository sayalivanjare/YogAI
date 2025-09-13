import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time
from pose_analysis import analyze_pose
from feedback.voice import VoiceFeedback

# ---------------- STREAMLIT SETUP ----------------
st.set_page_config(page_title="Yoga Pose Coach", layout="wide")
st.title("🧘 Yoga Pose Detection GUI")

# Pose selection
pose_name = st.selectbox("Select Pose:", ["tree", "tadasana", "namaste", "chair"])
feedback_interval = st.slider("Feedback Interval (seconds):", 1.0, 5.0, 2.5)

# Initialize voice
voice = VoiceFeedback(cooldown=feedback_interval)

# Mediapipe setup
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Placeholder for camera frame
frame_placeholder = st.image([])

# Initialize camera
cap = cv2.VideoCapture(0)
last_feedback_time = 0

st.write("Press 'Stop' button below to end the session.")

stop = st.button("Stop Session")

while cap.isOpened() and not stop:
    ret, frame = cap.read()
    if not ret:
        st.warning("Failed to read from camera.")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    overlay_text = ""
    h, w = frame.shape[:2]

    if results.pose_landmarks:
        # Draw landmarks
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
        )

        # Convert landmarks
        landmarks = {idx: (int(lm.x * w), int(lm.y * h), lm.z, lm.visibility)
                     for idx, lm in enumerate(results.pose_landmarks.landmark)}

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

    # Overlay text
    if overlay_text:
        color = (0, 0, 255) if "⚠️" in overlay_text else (0, 255, 0)
        cv2.putText(frame, overlay_text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, color, 2, cv2.LINE_AA)

    # Update Streamlit image
    frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

cap.release()
st.write("Session Ended. Thank you for practicing!")
