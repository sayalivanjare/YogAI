from gtts import gTTS
import time
import threading
import streamlit as st
import tempfile
import os

class VoiceFeedback:
    def __init__(self, cooldown=2.0):
        """
        Initializes voice feedback with a cooldown timer.
        cooldown: Minimum seconds between consecutive feedback.
        """
        self.cooldown = cooldown
        self.last_feedback_time = 0

    def speak(self, text):
        """
        Speaks the text if cooldown has passed.
        Runs speech in a separate thread to avoid blocking Streamlit updates.
        """
        current_time = time.time()
        if current_time - self.last_feedback_time >= self.cooldown:
            self.last_feedback_time = current_time
            print(f"🗣️ Voice: {text}")  # Debug log
            thread = threading.Thread(target=self._speak_thread, args=(text,))
            thread.start()

    def _speak_thread(self, text):
        try:
            # Generate speech
            tts = gTTS(text=text, lang='en')

            # Use a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                temp_path = tmp_file.name
                tts.save(temp_path)

            # Play in Streamlit
            with open(temp_path, "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3")

            # Clean up
            os.remove(temp_path)
        except Exception as e:
            print(f"⚠️ Voice feedback failed: {e}")
