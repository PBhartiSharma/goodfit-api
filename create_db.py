from datetime import datetime
from zoneinfo import ZoneInfo
import sqlite3
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)

def init_db():
    """
    Initializes the SQLite database:
    - Creates 'classes' and 'bookings' tables if they don't exist.
    - Seeds the 'classes' table with sample data (converted to UTC).
    """
    
    try:
        conn = sqlite3.connect("fitness.db")
        cursor = conn.cursor()

        # Create 'classes' table to store fitness class info
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                datetime TEXT NOT NULL,
                instructor TEXT NOT NULL,
                total_slots INTEGER,
                available_slots INTEGER
            )
        """)
        
        # Create 'bookings' table to store user bookings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER,
                client_name TEXT NOT NULL,
                client_email TEXT NOT NULL,
                FOREIGN KEY (class_id) REFERENCES classes(id)
            )
        """)

        # Seed classes with initial data
        cursor.execute("SELECT COUNT(*) FROM classes")
        if cursor.fetchone()[0] == 0:
            # Initial data in IST
            classes_ist = [
                ('Yoga', '2025-06-08 10:00:00', 'Ravi Sir', 5, 5),
                ('Zumba', '2025-06-08 18:00:00', 'Asha Mam', 8, 8),
                ('HIIT', '2025-06-09 07:00:00', 'Meera Mam', 10, 10),
                ('Strength Training', '2025-06-10 06:30:00', 'Nihal Sir', 2, 2),
                ('Dance Cardio', '2025-06-11 17:00:00', 'Sneha Mam', 5, 5),
            ]
            
            # Convert IST to UTC before inserting
            classes_utc = []
            for name, ist_str, instructor, total, available in classes_ist:
                ist_dt = datetime.strptime(ist_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=ZoneInfo("Asia/Kolkata"))
                utc_dt = ist_dt.astimezone(ZoneInfo("UTC"))
                classes_utc.append((name, utc_dt.isoformat(), instructor, total, available))

            # Insert converted data into the 'classes' table
            cursor.executemany("""
                INSERT INTO classes (name, datetime, instructor, total_slots, available_slots)
                VALUES (?, ?, ?, ?, ?)
            """, classes_utc)
            
        conn.commit()
        conn.close()
        
    except Exception as e :
        logging.error(f"Error during database initialization: {e}")




