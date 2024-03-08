# File: auth_service.py in the services/ directory

import sqlite3
import secrets

def register_user(username, password, role, email, fullname, db_file="phr_system.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Insert a new user
    cursor.execute("INSERT INTO users (username, password, role, email, fullname) VALUES (?, ?, ?, ?, ?)", 
                   (username, password, role, email, fullname))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    
    return user_id

def login_user(username, password, db_file="phr_system.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Verify user credentials
    cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    # Validate password and return user ID if successful
    if user and user[1] == password:
        return user[0]
    return None

def generate_token(user_id, db_file="phr_system.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Generate a new token
    token = secrets.token_urlsafe(32)
    cursor.execute("INSERT INTO tokens (token, user_id) VALUES (?, ?)", (token, user_id))
    conn.commit()
    conn.close()
    
    return token

def is_admin(user_id, db_file="phr_system.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] == 'admin' if result else False
    
    # if result and result[0] == 'admin':
    #     return True
    # return False


def verify_token(token, db_file="phr_system.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Check if the token exists and is valid
    cursor.execute("SELECT user_id FROM tokens WHERE token = ?", (token,))
    user_id = cursor.fetchone()
    conn.close()
    
    return user_id[0] if user_id else None
