Markdown

# 🛡️ SafeHealth AI – Real-Time Environmental Hazard Detection

This project implements a **Real-Time Environmental Hazard Detection** system using a custom-trained **YOLOv8** model and **Zero-Code Automation** for instant municipal alerting.
The system is designed to provide immediate alerts upon detection of critical environmental risks.

[![Project Status](https://img.shields.io/badge/Status-Hackathon_Success-brightgreen)](https://github.com/YourUsername/SafeHealth-AI)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Built with Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)](https://streamlit.io/)

---

## Project Overview 💡

SafeHealth AI transforms slow, reactive municipal response into **proactive health defense**. It leverages Computer Vision and webhooks to ensure swift action against hazards that lead to disease and infrastructural damage.

The model is trained to detect specific hazards:

- 🗑️ **Trash** (Risk of pollution, pests, and fire hazards)
- 💧 **Stagnant water** (Potential breeding ground for mosquitoes/disease)
- 🚧 **Blocked drain** (Risk of flooding and infrastructural damage)

---

## Key Features & Technical Innovation 🚀

| Feature | Technology | Innovation Focus |
| :--- | :--- | :--- |
| **Detection Core** | **Custom YOLOv8 Model** | High-accuracy identification on a unique dataset of hazards. |
| **Alert Automation** | **Webhooks + Zapier/IFTTT** | Instant, zero-code alerting, eliminating complex email server management. |
| **Data Reporting** | **Pandas & Tabulate** | Generates a clean, structured markdown table for official reports. |
| **Deployment** | **Streamlit Cloud** | Lightweight, easy-to-use web interface for field workers. |

---

## Tech Stack & Dependencies 🛠️

- **Language:** Python
- **Frameworks:** **PyTorch**, **Streamlit**
- **Computer Vision:** YOLOv8, OpenCV
- **Libraries:** Pandas, NumPy, python-dotenv, requests
- **Cloud Setup:** **`packages.txt`** (for Linux system dependencies like `libgl1`)

---

## How to Run Locally 

To set up and launch the application in your local environment:

### **1. Get the Code**
```bash
git clone [https://github.com/techylimat/SafeHealth-AI.git](https://github.com/techylimat/SafeHealth-AI.git)
cd SafeHealth-AI
2. Prepare Environment
Install dependencies:

Bash

pip install -r requirements.txt
pip install tabulate
Crucial Step: Ensure your model weights (best.pt) are in the root directory and managed by Git LFS if the file size exceeds 100MB.

3. Configure Secrets
Create a file named .env in the project root to store your automation URL:

# .env file content
ALERT_WEBHOOK_URL="[YOUR_SECRET_ZAPIER_OR_IFTTT_URL_HERE]"
4. Launch App
Bash

streamlit run apps/streamlit_app.py
Deployment Notes (Streamlit Cloud) ☁️
This project requires two critical configuration files for a successful cloud deployment:

packages.txt: This file is mandatory and must contain the system libraries needed for OpenCV to load correctly:

libgl1
Secrets: The ALERT_WEBHOOK_URL must be added manually to the Streamlit Cloud's Secrets panel (or in .streamlit/secrets.toml) for the application to function in the cloud.
