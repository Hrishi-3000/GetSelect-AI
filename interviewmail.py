
def send_interview_emails():
    import sqlite3
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    conn = sqlite3.connect('jd_cv_matching.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        c.name, 
        sc.email,
        jd.jd_title, 
        isch.interview_datetime
    FROM shortlisted_candidates sc
    JOIN candidates c ON sc.candidate_id = c.candidate_id
    JOIN job_descriptions jd ON sc.jd_id = jd.jd_id
    JOIN interview_schedule isch ON sc.candidate_id = isch.candidate_id AND sc.jd_id = isch.jd_id
    """)

    candidates = cursor.fetchall()
    conn.close()

    
    sender_email = "hriro894@gmail.com"
    password = "ssxu gwrk dknc gyhw"
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)

    for name, email, job_title, interview_time in candidates:
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email
        message['Subject'] = f"Interview Schedule for {job_title}"

        body = f"""
        Dear {name},

        Congratulations! You have been shortlisted for the role of {job_title}.

        Your interview is scheduled for: {interview_time}.

        Please be available on time. Let us know if you have any questions.

        Best regards,  
        HR Team
        """

        message.attach(MIMEText(body, 'plain'))
        server.send_message(message)
        print(f" Email sent to {name} ({email})")

    server.quit()
    print("📬 All interview emails sent!")
