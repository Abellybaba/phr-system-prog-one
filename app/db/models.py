from app.db import database

database_file = "phr_system.db"


sql_create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    email TEXT UNIQUE,
    fullname TEXT
);
"""

sql_create_tokens_table = """
CREATE TABLE IF NOT EXISTS tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    expiry TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
"""

# patients table 
sql_create_patients_table = """
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    assigned_doctor_id INTEGER,
    date_of_birth TEXT,
    gender TEXT,
    phone_number TEXT,
    emergency_contact TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (assigned_doctor_id) REFERENCES doctors(id)
);
"""

# health_records table
sql_create_health_records_table = """
CREATE TABLE IF NOT EXISTS health_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    record_type TEXT NOT NULL,
    summary TEXT,
    detailed_record_link TEXT,
    created_by_doctor_id INTEGER,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (created_by_doctor_id) REFERENCES doctors(id)
);
"""


sql_create_doctors_table = """
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    specialty TEXT,
    years_of_experience INTEGER,
    contact_info TEXT;
    user_id INTEGER NOT NULL,
    department_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
"""

sql_create_departments_table = """
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
"""

# Function to create tables
def setup_database():
    conn = database.create_connection(database_file)
    if conn is not None:
        database.create_table(conn, sql_create_users_table)
        database.create_table(conn, sql_create_departments_table)
        database.create_table(conn, sql_create_doctors_table)
        database.create_table(conn, sql_create_patients_table)
        database.create_table(conn, sql_create_health_records_table)
        database.create_table(conn, sql_create_tokens_table)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == "__main__":
    setup_database()
