import pandas as pd
import os
import re
from tqdm import tqdm
from scipy.stats import percentileofscore

# --- Helper functions ---
def extract_skills(text):
    keywords = [
        "Python", "Java", "C++", "JavaScript", "R", "SQL", "Scala", "Solidity", "C/C++", "Assembly Language",
        "TensorFlow", "PyTorch", "Scikit-learn", "React", "Node.js", "ROS", "AWS", "Azure", "Google Cloud",
        "Terraform", "CloudFormation", "Docker", "Kubernetes", "Ansible", "Chef", "Puppet", "CI/CD", "Hadoop",
        "Spark", "Kafka", "Distributed Computing", "MySQL", "PostgreSQL", "Oracle", "MongoDB", "SQL/NoSQL",
        "Ethereum", "Hyperledger", "Smart Contracts", "DApps", "SIEM", "Firewalls", "Intrusion Detection Systems",
        "Encryption", "Selenium", "JUnit", "TestNG", "Tableau", "Power BI", "Agile", "Scrum", "Waterfall", "DevOps",
        "Microservices", "Infrastructure-as-Code", "SDLC", "TCP/IP", "DNS", "DHCP", "VPNs", "Cisco", "Juniper",
        "Embedded Linux", "RTOS", "Microcontrollers", "Motion Planning", "Figma", "Adobe XD", "Sketch",
        "Machine Learning", "Deep Learning", "NLP", "Data Preprocessing", "Model Deployment", "RESTful APIs",
        "Git", "User Research", "Usability Testing", "Risk Management", "Compliance"
    ]
    text_lower = text.lower()
    return list({kw for kw in keywords if kw.lower() in text_lower})

def extract_years_experience(text):
    matches = re.findall(r"(\d+)\+?\s*(?:years|yrs|year)", text.lower())
    return int(max(matches, key=int)) if matches else 0

def experience_boost(years):
    if years >= 8: return 10
    elif years >= 5: return 7
    elif years >= 3: return 5
    elif years >= 1: return 3
    return 0

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else "Not found"

def extract_name(text):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    exclude_keywords = ["curriculum vitae", "resume", "cv", "contact", "email", "phone", "address", "linkedin", "github", "objective"]
    prefix_patterns = [
        r'^name:\s*', r'^full name:\s*', r'^candidate name:\s*', r'^applicant name:\s*', r'^name\s*',
    ]
    for i, line in enumerate(lines[:10]):
        if len(line) > 50:
            continue
        if any(keyword in line.lower() for keyword in exclude_keywords):
            continue
        cleaned_line = line
        for pattern in prefix_patterns:
            cleaned_line = re.sub(pattern, '', cleaned_line, flags=re.IGNORECASE).strip()
        words = cleaned_line.split()
        if 2 <= len(words) <= 4 and all(word[0].isupper() for word in words) and not any(word.isdigit() for word in words) and not any(word.endswith('.com') for word in words):
            return cleaned_line
    return "Not found"

# --- Main runner ---
def run():
    print("📄 Matching CVs to job descriptions...")

    jd_df = pd.read_csv("jd_summary_output.csv")
    cv_dir = "convytext"
    cv_files = [f for f in os.listdir(cv_dir) if f.endswith(".txt")]

    final_results = []

    for jd_idx, jd_row in tqdm(jd_df.iterrows(), total=len(jd_df), desc="Processing JDs"):
        jd_title = jd_row.get("Job Title", f"JD {jd_idx+1}")
        jd_skills = jd_row.get("Skills", "")
        jd_skills_lower = set([s.lower() for s in eval(jd_skills)]) if jd_skills else set()

        cv_scores = []

        for cv_file in tqdm(cv_files, desc=f"Matching CVs for JD {jd_idx+1}", leave=False):
            with open(os.path.join(cv_dir, cv_file), "r", encoding="utf-8") as f:
                cv_text = f.read()

            cv_skills = extract_skills(cv_text)
            cv_skills_lower = set([s.lower() for s in cv_skills])
            matched_skills = jd_skills_lower.intersection(cv_skills_lower)
            skill_match_count = len(matched_skills)

            years_exp = extract_years_experience(cv_text)
            exp_bonus = experience_boost(years_exp)
            email = extract_email(cv_text)
            name = extract_name(cv_text)

            cv_scores.append({
                "JD_ID": jd_idx + 1,
                "JD_Title": jd_title,
                "CV_File": cv_file,
                "Candidate_Name": name,
                "Matched_Skills_Count": skill_match_count,
                "Matched_Skills": list(matched_skills),
                "Years_Experience": years_exp,
                "Experience_Bonus": exp_bonus,
                "Email": email
            })

        match_counts = [entry["Matched_Skills_Count"] for entry in cv_scores]

        for entry in cv_scores:
            base_percentile = percentileofscore(match_counts, entry["Matched_Skills_Count"])
            final_score = min(base_percentile + entry["Experience_Bonus"], 100)
            entry["Skill_Match_Percentile"] = round(base_percentile, 2)
            entry["Final_Score"] = round(final_score, 2)
            entry["Selected"] = "Yes" if final_score >= 80 else "No"
            if entry["Selected"] == "No":
                entry["Email"] = ""

        final_results.extend(cv_scores)

    output_df = pd.DataFrame(final_results)
    output_df.to_csv("skill_experience_percentile_matching.csv", index=False)
    print("✅ Matching completed. Saved to skill_experience_percentile_matching.csv")
