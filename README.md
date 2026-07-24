Here is your cleaned-up, perfectly formatted, and professional **`README.md`** file.

The markdown syntax, directory trees, table formatting, and installation commands have been tidied up so you can copy and paste this directly into your GitHub repository root.

```markdown
# AI-Powered Personalized Networking Assistant

This project was developed as part of the **SmartBridge Internship Program** under the **Artificial Intelligence & Data Science** domain. The objective is to build an intelligent networking assistant that helps users generate personalized conversation starters based on event details using Natural Language Processing (NLP) and Generative AI techniques.

The application follows a decoupled architecture using **FastAPI** as the backend engine and **Streamlit** as the interactive frontend client. It utilizes **DistilBERT** for semantic theme extraction and **GPT-2 Small** for generating context-aware networking icebreakers.

---

## 🎯 Project Objective

The primary objective of this project is to assist professionals, students, and conference attendees in initiating meaningful conversations by generating personalized networking suggestions based on event topics and user interests.

---

## ✨ Key Features

* **AI-Powered Theme Extraction:** Contextual classification of event details into core networking themes.
* **Personalized Icebreaker Generation:** Autoregressive generation of context-aware conversation starters.
* **Interactive Streamlit Dashboard:** User-friendly frontend client for real-time input and rendering.
* **FastAPI REST Engine:** Decoupled backend architecture providing high-performance API endpoints.
* **Wikipedia Context Verification:** Automated background retrieval for topic fact-checking.
* **Telemetry & History Tracking:** Automatic logging of user interactions to persistent JSON stores.
* **User Feedback Collection:** Interactive feedback mechanisms for continuous response evaluation.
* **Automated QA Verification:** Continuous unit testing implemented via Pytest.

---

## 🛠️ Technology Stack

* **Programming Language:** Python
* **Frontend UI Framework:** Streamlit
* **Backend API Engine:** FastAPI, Uvicorn
* **Machine Learning Pipelines:** DistilBERT (Zero-Shot Classification), GPT-2 Small (Text Generation), Hugging Face Transformers
* **Data Storage:** Local JSON Flat-Files (`history.json`, `feedback.json`)
* **Testing & Quality Assurance:** Pytest
* **Deployment & Environment:**
  * **Current Implementation:** Decoupled Microservice Architecture (FastAPI on Port 8000, Streamlit on Port 8501 via Uvicorn)
  * **Production Target Roadmap:** Microservice Containerization (Docker), Semantic Vector Database (ChromaDB), Asynchronous Task Queue (Celery + Redis)

---

## 🧠 Machine Learning Workflow

1. **Theme Extraction:** DistilBERT is utilized through a Zero-Shot Classification pipeline to extract and categorize semantic themes from user-provided event information.
2. **Icebreaker Generation:** Extracted themes are injected into prompt templates and fed to GPT-2 Small, which generates tailored networking conversation starters using autoregressive inference layers.

---

## 📂 Project Directory & Milestone Map

This repository houses all institutional deliverables, with the functional application codebase integrated directly within the development phase folder:

```text
1. Brainstorming & Ideation/
├── Brainstorming & Idea Prioritization.pdf
├── Define Problem Statements.pdf
└── Empathy Map.pdf

2. Requirement Analysis/
├── Customer Journey Map.pdf
├── Data Flow Diagram.pdf
├── Solution Requirements.pdf
└── Technology Stack.pdf

3. Project Design Phase/
├── Problem-Solution Fit.pdf
├── Proposed Solution.pdf
└── Solution Architecture.pdf

4. Project Planning Phase/
└── Project Planning.pdf

5. Project Development Phase/
├── Code-Layout, Readability
├── Coding & Solution.pdf
├── backend/            <-- Core FastAPI Engine, models, and Wikipedia service
├── frontend/           <-- Streamlit UI dashboard interface layer
├── data/               <-- Local telemetry logging (history.json, feedback.json)
└── tests/              <-- Automated validation suite executed via pytest

6. Project Testing/
└── Performance Testing.pdf

7. Project Documentation/
├── Project Executable Files.pdf
└── Sample Project Documentation.pdf

8. Project Demonstration/
├── Communication.pdf
├── Scalability & Future Plan.pdf
└── Team Involvement.pdf

```

---

## 🚀 Installation & Setup Instructions

### 1. Clone the Repository

```cmd
git clone [https://github.com/yourusername/AI-Powered-Personalized-Networking-Assistant.git](https://github.com/yourusername/AI-Powered-Personalized-Networking-Assistant.git)
cd AI-Powered-Personalized-Networking-Assistant

```

### 2. Create and Activate a Virtual Environment

```cmd
python -m venv myenv
myenv\Scripts\activate

```

### 3. Install Workspace Dependencies

```cmd
pip install -r "5. Project Development Phase/backend/requirements.txt"

```

---

## ⚡ Running the Application

*Note: Paths are wrapped in quotes to safely handle institutional directory spaces.*

### Step 1: Initialize the FastAPI Backend Engine (Port 8000)

Open a terminal workspace, activate the environment, and execute:

```cmd
python "5. Project Development Phase/backend/app.py"

```

* **Swagger API Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc API Documentation:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Step 2: Launch the Streamlit Frontend UI (Port 8501)

Open a second terminal window, activate the environment, and run:

```cmd
streamlit run "5. Project Development Phase/frontend/app.py"

```

* **Interactive Web Dashboard:** [http://localhost:8501](http://localhost:8501)

---

## 🧪 Testing & Quality Assurance

To execute the automated unit testing suite across the application modules, run:

```cmd
python -m pytest "5. Project Development Phase/tests/"

```

---

## 📊 Scalability & Future Roadmap Grid

| Target Module | Implementation Strategy | Core Technology | Strategic Impact / Value |
| --- | --- | --- | --- |
| **Deployment** | Microservice Containerization | Docker | Eliminates environmental disparities and simplifies multi-server deployment. |
| **Data Layer** | Semantic Memory Migration | ChromaDB | Upgrades flat-file JSON storage to vector embeddings for sub-millisecond similarity lookups. |
| **Inference Queue** | Asynchronous Task Processing | Celery + Redis | Prevents UI blocking by executing heavy AI model inference in background workers. |

---

## 📽️ Project Deliverables & Demonstration

This repository contains all finalized SmartBridge submission deliverables across the project lifecycle, including milestone documentation, development source code, and continuous testing reports.

* 📺 **Project Demonstration Video:** [Watch the Video on YouTube](https://youtu.be/NPYMMxekIOQ?si=7Zdzcr9_6JEy2jFG)

---

## 👥 Team Members

* **Kaverigari Meghana** — Co-Developer, Systems Integration Engineer, & Project Documentation
* **C S Madhulika** — Team Leader, Co-Developer, & Project Documentation

---

## 🙏 Acknowledgements

This project was developed as part of the **SmartBridge Internship Program** under the guidance of our mentors. We sincerely acknowledge SmartBridge, our institution, and all mentors and evaluators whose continuous support, guidance, and feedback contributed to the successful completion of this project.

```

```
