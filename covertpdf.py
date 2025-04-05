import pandas as pd
import re
import spacy
nlp = spacy.load("en_core_web_sm")
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
def extract_skills(text):
    text_lower = text.lower()
    return list({kw for kw in skill_keywords if kw in text_lower})

def extract_qualifications(text):
    text_lower = text.lower()
    return list({kw for kw in qualification_keywords if kw in text_lower})

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

def parse_jd_csv(input_csv='job_description.csv', output_csv='jd_summary_output.csv'):
    df = pd.read_csv(input_csv, encoding='ISO-8859-1')

    summaries = []
    for idx, row in df.iterrows():
        summary = extract_summary(row['Job Description'])
        summary['Job Title'] = row['Job Title']
        summaries.append(summary)

    summary_df = pd.DataFrame(summaries)[['Job Title', 'Skills', 'Qualifications', 'Experience', 'Responsibilities']]
    summary_df.to_csv(output_csv, index=False)

    print(f" JD summaries extracted and saved to {output_csv}")
def run():
    import os
    from PyPDF2 import PdfReader

    input_dir = "CVs1"
    output_dir = "convytext"
    os.makedirs(output_dir, exist_ok=True)

    pdf_files = [f for f in os.listdir(input_dir) if f.endswith(".pdf")]

    for pdf_file in pdf_files:
        try:
            reader = PdfReader(os.path.join(input_dir, pdf_file))
            text = ''
            for page in reader.pages:
                text += page.extract_text() or ''

            output_filename = os.path.splitext(pdf_file)[0] + ".txt"
            output_path = os.path.join(output_dir, output_filename)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f" Converted: {pdf_file} -> {output_filename}")
        except Exception as e:
            print(f" Failed to convert {pdf_file}: {e}")
