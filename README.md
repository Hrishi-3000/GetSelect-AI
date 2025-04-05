#  GetSelect-AI

An AI-powered recruitment automation system built by **DuelBot** (Hrishikesh & Rohit) for **Accenture Hackathon 2025**.

---

##  Features

-  Automatically parses **Job Descriptions (JDs)** using NLP
-  Extracts and processes **resumes (CVs)** from PDFs
-  Calculates **AI-based match percentage** between JDs and CVs
-  Filters and **shortlists candidates** based on match threshold (e.g. ≥ 80%)
-  **Schedules interviews** for shortlisted candidates
-  Sends **personalized interview emails**
-  Interactive **Tkinter-based GUI dashboard**
-  Real-time **status, logs, and countdown timer**

---

## Architecture

GetSelect-AI uses a **modular multi-agent design**, each responsible for a specific task:

| Module                 | Responsibility                                                                 |
|------------------------|---------------------------------------------------------------------------------|
| `covertpdf.py`         | Converts resumes from PDF format to raw text and extracts structured info       |
| `JDParsing.py`         | Summarizes JDs and extracts key components like skills, qualifications, etc.    |
| `newmatric.py`         | Matches extracted resume data with JD and calculates match percentage           |
| `advanced_matching.py` | Stores shortlisted candidates in SQLite and handles advanced matching logic     |
| `schedular.py`         | Generates interview slots and schedules interviews for selected candidates      |
| `interviewmail.py`     | Sends interview confirmation emails to candidates with time, date & details     |
| `main.py`              | One-click GUI to control all steps with visual logs and interview timer         |

---

##  Requirements

Install all dependencies via:

```bash
pip install -r requirements.txt
