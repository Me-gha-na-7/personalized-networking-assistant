# 🤝 Personalized AI Networking Assistant

[![Streamlit App](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit)](https://personalized-networking-assistant.streamlit.app)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)](https://meghanaaa7-networking-assistant-backend.hf.space/docs)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Spaces-FFD21E?style=for-the-badge&logo=huggingface)](https://huggingface.co/spaces/meghanaaa7/networking-assistant-backend)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)

An end-to-end AI-powered assistant designed to help professionals generate personalized outreach messages, analyze networking events, and prepare tailored conversation starters using Natural Language Processing (NLP) models.

---

## 🚀 Live Demo & Endpoints

- **🎨 Frontend UI:** [Launch Streamlit Application](https://personalized-networking-assistant.streamlit.app)
- **⚡ Backend API Base:** `https://meghanaaa7-networking-assistant-backend.hf.space`
- **📖 API Documentation (Swagger):** [View FastAPI Docs](https://meghanaaa7-networking-assistant-backend.hf.space/docs)

---

## ✨ Features

- **📩 Personalized Outreach Generator:** Drafts context-aware cold emails and LinkedIn messages using fine-tuned Hugging Face NLP models.
- **🏷️ Event & Intent Classifier:** Uses DistilBERT models to classify networking events and target objectives.
- **💬 Interactive Streamlit Interface:** User-friendly frontend hosted on Streamlit Community Cloud.
- **⚡ Decoupled Microservice Architecture:** Streamlit frontend decoupled from the FastAPI backend running on Hugging Face Spaces CPU runtimes.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit, Requests
- **Backend:** FastAPI, Uvicorn, Pydantic
- **AI & NLP:** PyTorch, Hugging Face Transformers (`distilbert-base-uncased`, `gpt2`)
- **Hosting & Deployment:** Streamlit Community Cloud (Frontend), Hugging Face Spaces (Backend)

---

## 📁 Repository Structure

```text
personalized-networking-assistant/
├── backend/
│   ├── app.py             # FastAPI REST Endpoints & Inference Pipeline
│   └── requirements.txt   # Backend Dependencies (PyTorch, Transformers, FastAPI)
├── frontend/
│   ├── main.py            # Streamlit Application Interface
│   └── requirements.txt   # Frontend Dependencies
├── data/                  # Sample context and configuration files
└── README.md              # Project Documentation
