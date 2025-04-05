# GetSelect-AI


An AI-powered recruitment automation system built by **DuelBot** (Hrishikesh & Rohit) for Accenture Hackathon 2025.

---

## Features

-  Extracts and parses Job Descriptions
-  Parses resumes (CVs)
-  AI-based match percentage calculation
-  Shortlisting based on match threshold
-  Interview scheduler + email sender
-  One-click GUI dashboard
-  Real-time log + interview timer

---

##  Architecture

Multi-agent system:

- `covertpdf.py`: Resume reader
- `JDParsing.py`: JD summarizer
- `newmatric.py`: Matcher
- `advanced_matching.py`: Shortlisting logic
- `schedular.py`: Interview scheduler
- `interviewmail.py`: Email sender

---

##  Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
