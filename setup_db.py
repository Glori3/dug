import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('hospital_B.db')
cursor = conn.cursor()

# Create patients table
cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT UNIQUE,
                    name TEXT,
                    age INTEGER,
                    gender TEXT,
                    allergy TEXT,
                    symptoms TEXT,
                    fingerprint TEXT)''')

# Create allergies table
cursor.execute('''CREATE TABLE IF NOT EXISTS allergies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Patient_ID INTEGER,
                    Allergy_Name TEXT,
                    FOREIGN KEY (Patient_ID) REFERENCES patients(id) ON DELETE CASCADE)''')

# Create medications table
cursor.execute('''CREATE TABLE IF NOT EXISTS medications (
                    Medication_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Medication_Name TEXT,
                    Recommended_For TEXT)''')

# Create recommended_medications table
cursor.execute('''CREATE TABLE IF NOT EXISTS recommended_medications (
                    Record_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Patient_ID INTEGER,
                    Allergy_ID INTEGER,
                    Medication_ID INTEGER,
                    Dosage TEXT,
                    Duration TEXT,
                    Recovery_Time_Days INTEGER,
                    FOREIGN KEY (Patient_ID) REFERENCES patients(id) ON DELETE CASCADE,
                    FOREIGN KEY (Allergy_ID) REFERENCES allergies(id) ON DELETE CASCADE,
                    FOREIGN KEY (Medication_ID) REFERENCES medications(Medication_ID) ON DELETE CASCADE)''')

# Commit changes and close connection
conn.commit()
conn.close()

print("Database setup complete!")
