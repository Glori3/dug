from flask import Flask, render_template, request, jsonify
import sqlite3
import pickle
import numpy as np

app = Flask(__name__)

# Load trained model for medication recommendation
with open('rf_model.pkl', 'rb') as model_file:
    rf_model = pickle.load(model_file)

# Database initialization
conn = sqlite3.connect('hospital_A.db', check_same_thread=False)
cursor = conn.cursor()
# Create patient table
cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT UNIQUE,
                    name TEXT,
                    age INTEGER,
                    gender TEXT,
                    allergy TEXT,
                    symptoms TEXT,
                    fingerprint TEXT)''')
conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

# Route to register new patients
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    patient_id = data['patient_id']
    name = data['name']
    age = data['age']
    gender = data['gender']
    allergy = data['allergy']
    symptoms = data['symptoms']
    fingerprint = data['fingerprint']  # Simulated fingerprint data
    
    try:
        cursor.execute("INSERT INTO patients (patient_id, name, age, gender, allergy, symptoms, fingerprint) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (patient_id, name, age, gender, allergy, symptoms, fingerprint))
        conn.commit()
        return jsonify({'message': 'Patient registered successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Route to retrieve patient details using fingerprint for emergency cases
@app.route('/emergency_lookup', methods=['POST'])
def emergency_lookup():
    data = request.get_json()
    fingerprint = data['fingerprint']
    cursor.execute("SELECT * FROM patients WHERE fingerprint = ?", (fingerprint,))
    patient = cursor.fetchone()
    if patient:
        return jsonify({'patient_id': patient[1], 'name': patient[2], 'age': patient[3], 'gender': patient[4], 'allergy': patient[5], 'symptoms': patient[6]})
    else:
        return jsonify({'error': 'Patient not found in Hospital A'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Running on port 5001 for Hospital A
