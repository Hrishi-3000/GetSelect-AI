import pandas as pd
import re
import spacy

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Keywords
skill_keywords = [kw.lower() for kw in [
    "Python", "Java", "C++", "JavaScript", "R", "SQL", "Scala", "Solidity", "C/C++", "Assembly Language",
    "TensorFlow", "PyTorch", "Scikit-learn", "React", "Node.js", "ROS", "AWS", "Azure", "Google Cloud",
    "Terraform", "CloudFormation", "Docker", "Kubernetes", "Ansible", "Chef", "Puppet", "CI/CD", "Hadoop",
    "Spark", "Kafka", "Distributed Computing", "MySQL", "PostgreSQL", "Oracle", "MongoDB", "SQL/NoSQL",
    "Ethereum", "Hyperledger", "Smart Contracts", "DApps", "SIEM", "Firewalls", "Intrusion Detection Systems",
    "Encryption", "Selenium", "JUnit", "TestNG", "Tableau", "Power BI", "Agile", "Scrum", "Waterfall",
    "DevOps", "Microservices", "Infrastructure-as-Code", "SDLC", "TCP/IP", "DNS", "DHCP", "VPNs", "Cisco",
    "Juniper", "Embedded Linux", "RTOS", "Microcontrollers", "Motion Planning", "Figma", "Adobe XD", "Sketch",
    "Machine Learning", "Deep Learning", "NLP", "Data Preprocessing", "Model Deployment", "RESTful APIs",
    "Git", "User Research", "Usability Testing", "Risk Management", "Compliance"
]]
qualification_keywords = ["bachelor", "master", "ph.d", "mba", "diploma"]
experience_pattern = r"(\d+)\+?\s*(?:years|yrs)"

# --- Extractors ---
def extract_skills(text):
    return list({kw for kw in skill_keywords if kw in text.lower()})

def extract_qualifications(text):
    return list({kw for kw in qualification_keywords if kw in text.lower()})

def extract_experience(text):
    matches = re.findall(experience_pattern, text.lower())
    return f"{max(map(int, matches))} years" if matches else "Not specified"

def extract_summary(text):
    doc = nlp(text)
    skills = extract_skills(text)
    qualifications = extract_qualifications(text)
    experience = extract_experience(text)
    sentences = [sent.text for sent in doc.sents if "responsib" in sent.text.lower()]
    responsibilities = sentences[:2] if sentences else ["Not clearly mentioned"]
    
    return {
        "Skills": skills,
        "Qualifications": qualifications,
        "Experience": experience,
        "Responsibilities": responsibilities
    }

# --- Run Function ---
def run():
    print("🔍 Parsing job descriptions...")

    # Load CSV
    df = pd.read_csv("job_description.csv", encoding='ISO-8859-1')

    summaries = []

    for idx, row in df.iterrows():
        summary = extract_summary(row['Job Description'])
        summary['Job Title'] = row['Job Title']
        summaries.append(summary)

    summary_df = pd.DataFrame(summaries)[['Job Title', 'Skills', 'Qualifications', 'Experience', 'Responsibilities']]
    summary_df.to_csv("jd_summary_output.csv", index=False)

    print("✅ JD summary saved to jd_summary_output.csv")
