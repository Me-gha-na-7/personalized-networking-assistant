# AI-Powered Personalized Networking Assistant

This project was developed as part of the SmartBridge Internship Program under the Artificial Intelligence & Data Science domain. The objective is to build an intelligent networking assistant that helps users generate personalized conversation starters based on event details using Natural Language Processing (NLP) and Generative AI techniques.

The application follows a decoupled architecture using FastAPI as the backend and Streamlit as the frontend. It utilizes DistilBERT for semantic theme extraction and GPT-2 Small for generating context-aware networking icebreakers.

---

## Project Objective

The primary objective of this project is to assist professionals, students, and conference attendees in initiating meaningful conversations by generating personalized networking suggestions based on event topics and user interests.

---

## Key Features

* AI-powered semantic theme extraction
* Personalized networking icebreaker generation
* Interactive Streamlit dashboard
* FastAPI REST API backend
* Wikipedia-based contextual information
* User history tracking
* Feedback collection system
* Automated testing using Pytest

---

## Technology Stack

## Technology Stack

* **Programming Language:** Python
* **Frontend:** Streamlit
* **Backend:** FastAPI, Uvicorn
* **Machine Learning:** DistilBERT (Zero-Shot Classification), GPT-2 Small (Text Generation), Hugging Face Transformers
* **Data Storage:** Local JSON Flat-Files (Telemetry & Feedback Logging)
* **Testing & Quality Assurance:** Pytest
* **Deployment & Hosting Environment:**

  * **Local Environment:** Decoupled Microservice Architecture (FastAPI running on Port **8000** and Streamlit running on Port **8501** using Uvicorn)
  * **Production Target Roadmap:**

    * Docker Containerization
    * ChromaDB (Vector Database Migration)
    * Celery + Redis (Asynchronous Task Queue Management)


---

## Machine Learning Workflow

1. **Theme Extraction:** DistilBERT is used through a Zero-Shot Classification pipeline to identify semantic themes from user-provided event information.
2. **Icebreaker Generation:** The extracted themes are provided as templates to GPT-2 Small, which generates personalized networking conversation starters using autoregressive inference layers.

---

## Project Directory & Milestone Map

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

## Installation & Setup Instructions

### 1. Clone the Repository

```cmd
git clone https://github.com/yourusername/AI-Powered-Personalized-Networking-Assistant.git
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

## Running the Project

> **Note:** Folder paths are wrapped in quotes to safely handle spaces in directory names.

### Step 1: Start the FastAPI Backend (Port 8000)

Open a terminal, activate the virtual environment, and execute:

```cmd
python "5. Project Development Phase/backend/app.py"
```

Access the API documentation:

* **Swagger UI:** http://127.0.0.1:8000/docs
* **ReDoc:** http://127.0.0.1:8000/redoc

### Step 2: Launch the Streamlit Frontend (Port 8501)

Open another terminal, activate the environment, and run:

```cmd
streamlit run "5. Project Development Phase/frontend/app.py"
```

Open the application in your browser:

* **Streamlit UI:** http://localhost:8501

---

## Testing & Quality Assurance

Run the automated testing suite using:

```cmd
python -m pytest "5. Project Development Phase/tests/"
```

---

## Scalability & Future Roadmap

| Target Module       | Implementation Strategy       | Core Technology | Strategic Impact                                                                       |
| ------------------- | ----------------------------- | --------------- | -------------------------------------------------------------------------------------- |
| **Deployment**      | Microservice Containerization | Docker          | Eliminates environment inconsistencies and simplifies deployment.                      |
| **Data Layer**      | Semantic Memory Migration     | ChromaDB        | Replaces JSON storage with vector embeddings for semantic search and faster retrieval. |
| **Inference Queue** | Asynchronous Processing       | Celery + Redis  | Prevents UI blocking by executing AI inference in distributed background workers.      |

---

## Project Deliverables & Demonstration

This repository contains all finalized SmartBridge submission deliverables across the project lifecycle, including project documentation, development artifacts, source code, and testing reports.

**Project Demonstration Video (Unlisted YouTube):**

```text
https://youtu.be/NPYMMxekIOQ?si=7Zdzcr9_6JEy2jFG
```

---

## Team Members

* **Kaverigari Meghana** – Co-Developer & Systems Integration Engineer
* **Madhulika** – Team Leader & Co-Developer

---

## Acknowledgement

This project was developed as part of the SmartBridge Internship Program under the guidance of our faculty mentors. We sincerely acknowledge SmartBridge, our institution, and all mentors and evaluators whose continuous support, guidance, and feedback contributed to the successful completion of this project.
