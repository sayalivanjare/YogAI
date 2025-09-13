````markdown
# 🧘 YogAI — Real-Time Yoga Pose Detection & Correction

[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)  
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red)](https://streamlit.io/)  

---

## **🌟 Project Overview**
**YogAI** is a real-time yoga posture detection system that combines **computer vision** (MediaPipe + OpenCV) with a **smart pressure mat**.  
It analyzes user posture, detects misalignments, and provides **instant visual and voice feedback** through an interactive **Streamlit GUI**.  

---

## **🎯 Key Features**
- **Vision + Pressure Mat Fusion** – Accurate detection using camera & mat data  
- **Real-Time Feedback** – Supports Tree Pose, Tadasana, Namaste, Chair Pose  
- **Voice Guidance** – Hands-free instructions with `pyttsx3`  
- **Interactive GUI** – Live camera feed & posture overlays  
- **Extensible** – Easily add new poses or connect to a mobile app  

---

## **💻 Tech Stack**
- **Python** – Core logic  
- **OpenCV + Mediapipe** – Pose estimation  
- **Streamlit** – GUI & dashboard  
- **Pyttsx3** – Voice feedback  
- **Velostat + Microcontroller (ESP32/Arduino)** – Pressure sensing  

---

## **⚡ Installation & Setup**
1. Clone the repository:
```bash
git clone https://github.com/sayalivanjare/yoga-pose-coach.git
cd yoga-pose-coach
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

---

## **📝 Usage**

* Select the yoga pose from the dropdown menu
* Adjust feedback interval if needed
* Live camera feed shows your posture with corrections
* Voice guidance provides real-time tips for alignment

---

## **🤝 Contributing**

* Fork the repository → make your changes → submit a pull request
* Open to adding new poses or improving detection algorithms

---

## **📜 License**

Educational purposes only.

---

## **🔗 GitHub Repository**

[https://github.com/sayalivanjare/yoga-pose-coach](https://github.com/sayalivanjare/yoga-pose-coach)

```
