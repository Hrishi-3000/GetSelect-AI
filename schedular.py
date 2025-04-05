# schedular.py

def schedule_interviews():
    import sqlite3
    from datetime import datetime, timedelta

    conn = sqlite3.connect("jd_cv_matching.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT sc.candidate_id, sc.jd_id
        FROM shortlisted_candidates sc
        LEFT JOIN interview_schedule isch
        ON sc.candidate_id = isch.candidate_id AND sc.jd_id = isch.jd_id
        WHERE isch.interview_id IS NULL
    ''')

    shortlisted = cursor.fetchall()
    start_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)

    while start_time.weekday() > 4:
        start_time += timedelta(days=1)

    interviews_per_day = 8
    slot_duration = timedelta(minutes=30)
    slots_today = 0

    for candidate_id, jd_id in shortlisted:
        interview_time = start_time.strftime("%Y-%m-%d %H:%M")

        cursor.execute('''
            INSERT INTO interview_schedule (candidate_id, jd_id, interview_datetime)
            VALUES (?, ?, ?)
        ''', (candidate_id, jd_id, interview_time))

        start_time += slot_duration
        slots_today += 1

        if slots_today >= interviews_per_day:
            start_time += timedelta(days=1)
            while start_time.weekday() > 4:
                start_time += timedelta(days=1)
            start_time = start_time.replace(hour=10, minute=0)
            slots_today = 0

    conn.commit()
    conn.close()
    print("✅ Interview scheduling complete.")
