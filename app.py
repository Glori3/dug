from flask import Flask, render_template, request, jsonify
import sqlite3
import requests

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('hospital_B.db')
    conn.row_factory = sqlite3.Row
    return conn

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
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patients (patient_id, name, age, gender, allergy, symptoms, fingerprint) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (patient_id, name, age, gender, allergy, symptoms, fingerprint))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Patient registered successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Route to login using fingerprint and retrieve patient data
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    fingerprint = data['fingerprint']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE fingerprint = ?", (fingerprint,))
    patient = cursor.fetchone()
    
    if patient:
        # Fetch allergy details and recommended medications for the patient
        cursor.execute("SELECT * FROM allergies WHERE Patient_ID = ?", (patient['id'],))
        allergy = cursor.fetchall()
        
        cursor.execute("SELECT * FROM recommended_medications WHERE Patient_ID = ?", (patient['id'],))
        medications = cursor.fetchall()
        
        patient_data = {
            'patient_id': patient['patient_id'],
            'name': patient['name'],
            'age': patient['age'],
            'gender': patient['gender'],
            'allergy': allergy,
            'medications': medications
        }
        conn.close()
        return jsonify(patient_data)
    else:
        conn.close()
        return jsonify({'error': 'Patient not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Running on port 5002 for Hospital B
