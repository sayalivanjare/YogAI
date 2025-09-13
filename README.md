
# 🧘 YogAI — Real-Time Yoga Pose Detection & Correction

[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)  
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red)](https://streamlit.io/)  
[![License](https://img.shields.io/badge/License-Educational-green)](#)

---

## 🌟 Project Overview
**YogAI** is an intelligent yoga posture detection and correction system combining:  

- **Computer Vision**: Real-time pose estimation using **MediaPipe + OpenCV**  
- **Smart Pressure Mat**: Using **Velostat + ESP32/Arduino** for weight distribution analysis  

It provides **instant visual and voice feedback**, helping users maintain correct posture while practicing yoga. Ideal for both beginners and advanced practitioners.

📹 **Demo Video**: *(Replace with your demo link)*  
![Demo GIF](assets/demo.gif)

---

## 🎯 Key Features
| Feature | Description |
|---------|-------------|
| 🌐 Vision + Pressure Fusion | Accurate detection using camera + mat data |
| ⏱️ Real-Time Feedback | Detects & corrects Tree Pose, Tadasana, Namaste, Chair Pose |
| 🔊 Voice Guidance | Hands-free instructions using `pyttsx3` |
| 🖥️ Interactive GUI | Live camera feed with overlay & posture correction tips |
| 🔧 Extensible | Easily add new poses or connect to a mobile app |

---

## 💻 Tech Stack
| Component | Technology |
|-----------|------------|
| Core Logic | Python |
| Pose Detection | OpenCV + MediaPipe |
| GUI | Streamlit |
| Voice Feedback | pyttsx3 |
| Pressure Mat | Velostat + ESP32/Arduino |

---

## ⚡ Installation & Setup
1. **Clone the repository**
```bash
git clone https://github.com/sayalivanjare/yoga-pose-coach.git
cd yoga-pose-coach
````

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the Streamlit app**

```bash
streamlit run app.py
```

---

## 📝 Usage

1. Launch the app and select a yoga pose from the dropdown menu
2. Follow the **live camera feed overlay** for posture alignment
3. Listen to **voice guidance** for corrections
4. Practice regularly and track your improvements

---

## 📸 Screenshots / Demo Images

*(Add your images in the `assets` folder for clarity)*

| Tree Pose                          | Namaste Pose                   | Chair Pose                           |
| ---------------------------------- | ------------------------------ | ------------------------------------ |
| ![Tree Pose](assets/tree_pose.png) | ![Namaste](assets/namaste.png) | ![Chair Pose](assets/chair_pose.png) |

---

## 🤝 Contributing

* Fork the repository → make changes → submit a pull request
* Open to adding **new poses**, improving detection logic, or enhancing the GUI

---

## 📜 License

This project is for **educational purposes only**.

---

## 🔗 GitHub Repository

[https://github.com/sayalivanjare/yoga-pose-coach](https://github.com/sayalivanjare/yoga-pose-coach)

---

### 💡 Tips to Make It Even Better

* Add **short GIFs** for each yoga pose for better visualization
* Add a **YouTube/Loom demo video** for live interaction showcase
* Include more badges: Python version, Streamlit version, last updated
* Keep your `assets` folder organized with all screenshots and GIFs

---
