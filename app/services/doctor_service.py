# File: doctor_service.py in the services/ directory

import sqlite3
from app.services import auth_service
from app.services import doctor_service

def add_doctor(user_id, department_id, specialty, years_of_experience, contact_info, db_file="phr_system.db"):
    # Check if the user has admin privileges
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    user_role = cursor.fetchone()

    if user_role[0] != 'admin':
        conn.close()
        return None  # Or raise an exception

    # Proceed with adding the doctor if the user is an admin
    cursor.execute("INSERT INTO doctors (user_id, department_id, specialty, years_of_experience, contact_info) VALUES (?, ?, ?, ?, ?)", 
                   (user_id, department_id, specialty, years_of_experience, contact_info))
    conn.commit()
    doctor_id = cursor.lastrowid
    conn.close()

    return doctor_id

def assign_doctor_to_patient(doctor_id, patient_id, db_file="phr_system.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE patients SET assigned_doctor_id = ? WHERE id = ?", (doctor_id, patient_id))
    conn.commit()
    conn.close()

def update_doctor(user_id, doctor_id, department_id, specialty, years_of_experience, contact_info, db_file="phr_system.db"):
    if not auth_service.is_admin(user_id):
        return False  # Or raise an exception

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("UPDATE doctors SET department_id = ?, specialty = ?, years_of_experience = ?, contact_info = ? WHERE id = ?", 
                   (department_id, specialty, years_of_experience, contact_info, doctor_id))
    conn.commit()
    updated_rows = cursor.rowcount
    conn.close()
    
    return updated_rows > 0

def delete_doctor(user_id, doctor_id, db_file="phr_system.db"):
    if not auth_service.is_admin(user_id):
        return False  # Or raise an exception

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    
    return deleted_rows > 0


def get_doctor(doctor_id, db_file="phr_system.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
    doctor = cursor.fetchone()
    conn.close()
    
    return doctor
