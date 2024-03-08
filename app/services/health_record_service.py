# File: health_record_service.py in the services/ directory

import sqlite3

def add_health_record(patient_id, record_type, summary, detailed_record_link, created_by_doctor_id, db_file="phr_system.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO health_records (patient_id, record_type, summary, detailed_record_link, created_by_doctor_id) VALUES (?, ?, ?, ?, ?)", 
                   (patient_id, record_type, summary, detailed_record_link, created_by_doctor_id))
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    
    return record_id

def get_health_records(db_file="phr_system.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""SELECT hr.*, p.user_id, p.assigned_doctor_id, p.date_of_birth, p.gender, p.phone_number, p.emergency_contact 
                      FROM health_records hr
                      JOIN patients p ON hr.patient_id = p.id""")
    records = cursor.fetchall()
    conn.close()
    
    return [{
        'record_id': row[0],
        'patient_id': row[1],
        'record_type': row[2],
        'summary': row[3],
        'detailed_record_link': row[4],
        'created_by_doctor_id': row[5],
        'date': row[6],
        'user_id': row[7],
        'assigned_doctor_id': row[8],
        'date_of_birth': row[9],
        'gender': row[10],
        'phone_number': row[11],
        'emergency_contact': row[12]
    } for row in records]


def update_health_record(record_id, patient_id, record_type, summary, detailed_record_link, created_by_doctor_id, db_file="phr_system.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("UPDATE health_records SET patient_id = ?, record_type = ?, summary = ?, detailed_record_link = ?, created_by_doctor_id = ? WHERE id = ?",
                   (patient_id, record_type, summary, detailed_record_link, created_by_doctor_id, record_id))
    conn.commit()
    conn.close()

def delete_health_record(record_id, db_file="phr_system.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM health_records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

def get_health_record_by_id(record_id, db_file="phr_system.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM health_records WHERE id = ?", (record_id,))
    record = cursor.fetchone()
    conn.close()
    return record