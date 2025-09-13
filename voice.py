import pyttsx3
import time
import threading

class VoiceFeedback:
    def __init__(self, cooldown=2.0):
        """
        Initializes the voice engine with a cooldown timer.
        cooldown: Minimum seconds between two consecutive voice outputs.
        """
        self.engine = pyttsx3.init()
        self.cooldown = cooldown
        self.last_feedback_time = 0

        # Optional: set voice properties
        self.engine.setProperty('rate', 160)    # Speed of speech
        self.engine.setProperty('volume', 1.0)  # Volume 0.0 to 1.0

    def speak(self, text):
        """
        Speaks the text if cooldown has passed.
        Runs speech in a separate thread to avoid blocking Streamlit updates.
        """
        current_time = time.time()
        if current_time - self.last_feedback_time >= self.cooldown:
            self.last_feedback_time = current_time
            print(f"🗣️ Voice: {text}")  # Debug log

            # Use threading to avoid blocking
            thread = threading.Thread(target=self._speak_thread, args=(text,))
            thread.start()

    def _speak_thread(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"⚠️ Voice feedback failed: {e}")
