import sqlite3
import pandas as pd

def run():
    print("📊 Populating database with structured candidate-job match data...")

    # Load CSV
    csv_file = "skill_experience_percentile_matching.csv"
    df = pd.read_csv(csv_file)

    # Connect to SQLite database
    conn = sqlite3.connect("jd_cv_matching.db")
    cursor = conn.cursor()

    # --- TABLE CREATION ---
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS job_descriptions (
        jd_id INTEGER PRIMARY KEY,
        jd_title TEXT
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        cv_file TEXT,
        years_experience REAL
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS match_scores (
        match_id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        jd_id INTEGER,
        matched_skills_count INTEGER,
        matched_skills TEXT,
        skill_match_percentile REAL,
        experience_bonus REAL,
        final_score REAL,
        FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id),
        FOREIGN KEY (jd_id) REFERENCES job_descriptions(jd_id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS shortlisted_candidates (
        candidate_id INTEGER,
        jd_id INTEGER,
        email TEXT,
        final_score REAL,
        PRIMARY KEY(candidate_id, jd_id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interview_schedule (
        interview_id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        jd_id INTEGER,
        interview_datetime TEXT
    )''')

    # --- CACHES TO AVOID DUPLICATES ---
    jd_to_id = {}
    email_to_candidate_id = {}

    # --- INSERT DATA ---
    for _, row in df.iterrows():
        jd_id = int(row['JD_ID'])
        jd_title = row['JD_Title']
        name = row['Candidate_Name']
        email = row['Email']
        cv_file = row['CV_File']
        years_exp = row['Years_Experience']
        matched_skills_count = int(row['Matched_Skills_Count'])
        matched_skills = str(row['Matched_Skills'])
        exp_bonus = row['Experience_Bonus']
        skill_percentile = row['Skill_Match_Percentile']
        final_score = row['Final_Score']
        selected = row['Selected']

        # Insert JD
        if jd_id not in jd_to_id:
            cursor.execute('INSERT OR IGNORE INTO job_descriptions (jd_id, jd_title) VALUES (?, ?)', (jd_id, jd_title))
            jd_to_id[jd_id] = jd_title

        # Insert candidate
        if email not in email_to_candidate_id:
            cursor.execute('INSERT INTO candidates (name, email, cv_file, years_experience) VALUES (?, ?, ?, ?)',
                        (name, email, cv_file, years_exp))
            candidate_id = cursor.lastrowid
            email_to_candidate_id[email] = candidate_id
        else:
            candidate_id = email_to_candidate_id[email]

        # Insert match score
        cursor.execute('''
            INSERT INTO match_scores (
                candidate_id, jd_id, matched_skills_count, matched_skills,
                skill_match_percentile, experience_bonus, final_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            candidate_id, jd_id, matched_skills_count, matched_skills,
            skill_percentile, exp_bonus, final_score
        ))

        # Shortlisted candidates
        if selected == "Yes":
            cursor.execute('''
                INSERT OR IGNORE INTO shortlisted_candidates (candidate_id, jd_id, email, final_score)
                VALUES (?, ?, ?, ?)
            ''', (candidate_id, jd_id, email, final_score))

    # Finalize
    conn.commit()
    conn.close()

    print("✅ Database successfully populated with all structured data.")
