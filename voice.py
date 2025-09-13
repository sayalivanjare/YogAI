import pyttsx3
import time

class VoiceFeedback:
    def __init__(self, cooldown=2.0):
        self.engine = pyttsx3.init()
        self.last_feedback_time = 0
        self.cooldown = cooldown

    def speak(self, text):
        """Speaks the text if cooldown has passed."""
        current_time = time.time()
        if current_time - self.last_feedback_time >= self.cooldown:
            print("🗣️ Voice:", text)  # debug log
            self.engine.say(text)
            self.engine.runAndWait()
            self.last_feedback_time = current_time
