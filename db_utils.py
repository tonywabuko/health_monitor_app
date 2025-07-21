import sqlite3
import streamlit as st
from passlib.hash import pbkdf2_sha256  # For password hashing

# Database setup
def init_db():
    conn = sqlite3.connect('health_app.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 email TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL,
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Health data table
    c.execute('''CREATE TABLE IF NOT EXISTS health_data
                 (user_id INTEGER,
                  heart_rate REAL,
                  spo2 REAL,
                  temperature REAL,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

# User management
def create_user(name, email, password):
    conn = sqlite3.connect('health_app.db')
    c = conn.cursor()
    hashed_pw = pbkdf2_sha256.hash(password)
    try:
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                 (name, email, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Email already exists
    finally:
        conn.close()

def verify_user(email, password):
    conn = sqlite3.connect('health_app.db')
    c = conn.cursor()
    c.execute("SELECT id, name, password FROM users WHERE email=?", (email,))
    result = c.fetchone()
    conn.close()
    
    if result and pbkdf2_sha256.verify(password, result[2]):
        return {'id': result[0], 'name': result[1]}
    return None

# Health data operations
def save_health_data(user_id, heart_rate, spo2, temperature):
    conn = sqlite3.connect('health_app.db')
    c = conn.cursor()
    c.execute("""INSERT INTO health_data 
                 (user_id, heart_rate, spo2, temperature) 
                 VALUES (?, ?, ?, ?)""",
              (user_id, heart_rate, spo2, temperature))
    conn.commit()
    conn.close()

def get_user_health_history(user_id):
    conn = sqlite3.connect('health_app.db')
    c = conn.cursor()
    c.execute("""SELECT heart_rate, spo2, temperature, timestamp 
                 FROM health_data 
                 WHERE user_id=? 
                 ORDER BY timestamp DESC""", (user_id,))
    data = c.fetchall()
    conn.close()
    return data
