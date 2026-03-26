import psycopg2
import os

def get_connection():
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))
    return connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL
        );
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            expense_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id),
            amount DECIMAL(10, 2) NOT NULL,
            category VARCHAR(100) NOT NULL,
            description TEXT,
            date DATE NOT NULL
        );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()