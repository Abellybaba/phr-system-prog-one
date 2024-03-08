
import sqlite3

def add_patient(user_id, assigned_doctor_id, date_of_birth, gender, phone_number, emergency_contact, db_file="phr_system.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients (user_id, assigned_doctor_id, date_of_birth, gender, phone_number, emergency_contact) 
        VALUES (?, ?, ?, ?, ?, ?)""", (user_id, assigned_doctor_id, date_of_birth, gender, phone_number, emergency_contact))
    conn.commit()
    patient_id = cursor.lastrowid
    conn.close()
    return patient_id

def update_patient(patient_id, assigned_doctor_id, date_of_birth, gender, phone_number, emergency_contact, db_file="phr_system.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE patients 
        SET assigned_doctor_id = ?, date_of_birth = ?, gender = ?, phone_number = ?, emergency_contact = ? 
        WHERE id = ?""", (assigned_doctor_id, date_of_birth, gender, phone_number, emergency_contact, patient_id))
    conn.commit()
    conn.close()

def get_all_patients(db_file="phr_system.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return [{'id': row[0], 'user_id': row[1], 'assigned_doctor_id': row[2], 'date_of_birth': row[3], 'gender': row[4], 'phone_number': row[5], 'emergency_contact': row[6]} for row in patients]

def get_patient_by_id(patient_id, db_file="phr_system.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = cursor.fetchone()
    conn.close()
    if patient:
        return {'id': patient[0], 'user_id': patient[1], 'assigned_doctor_id': patient[2], 'date_of_birth': patient[3], 'gender': patient[4], 'phone_number': patient[5], 'emergency_contact': patient[6]}
    return None

def delete_patient(patient_id, db_file="phr_system.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    conn.commit()
    conn.close()

