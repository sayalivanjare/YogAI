import cv2
import mediapipe as mp
import time
from pose_analysis import analyze_pose
from voice import VoiceFeedback

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def run_pose_detection(camera_index=0, feedback_interval=2.5):
    cap = cv2.VideoCapture(camera_index)
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    voice = VoiceFeedback(cooldown=feedback_interval)

    last_feedback_time = 0
    pose_name = "tree"  # default pose

    print("📸 Starting Yoga Pose Detection")
    print("Press keys to switch poses: 1-Tree, 2-Tadasana, 3-Namaste, 4-Chair")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

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
            h, w = frame.shape[:2]
            landmarks = {idx: (int(lm.x * w), int(lm.y * h), lm.z, lm.visibility)
                         for idx, lm in enumerate(results.pose_landmarks.landmark)}

            # Feedback with proper delay
            current_time = time.time()
            if current_time - last_feedback_time >= feedback_interval:
                issues = analyze_pose(landmarks, pose_name)
                if issues:
                    overlay_text = "⚠️ " + ", ".join(issues)
                    print(f"[{pose_name.upper()}] {overlay_text}")
                    voice.speak(", ".join(issues))
                else:
                    overlay_text = "✅ Good posture"
                    print(f"[{pose_name.upper()}] {overlay_text}")
                    voice.speak("Good posture, keep going")
                last_feedback_time = current_time

        # Overlay text
        if overlay_text:
            cv2.putText(frame, overlay_text, (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255) if "⚠️" in overlay_text else (0, 255, 0),
                        2, cv2.LINE_AA)

        cv2.imshow("Yoga Pose Detection", frame)

        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC to quit
            break
        elif key == ord('1'):
            pose_name = "tree"
            print("🌳 Switched to Tree Pose")
        elif key == ord('2'):
            pose_name = "tadasana"
            print("🏔️ Switched to Mountain Pose")
        elif key == ord('3'):
            pose_name = "namaste"
            print("🙏 Switched to Namaste Pose")
        elif key == ord('4'):
            pose_name = "chair"
            print("🪑 Switched to Chair Pose")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_pose_detection()

