from flask import Flask, render_template, request, jsonify
import sqlite3
import requests

app = Flask(__name__)

# Database initialization
def get_db_connection():
    conn = sqlite3.connect('hospital_B.db')
    conn.row_factory = sqlite3.Row  # To access columns by name
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
        cursor.execute('''INSERT INTO patients (patient_id, name, age, gender, allergy, symptoms, fingerprint) 
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                       (patient_id, name, age, gender, allergy, symptoms, fingerprint))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Patient registered successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Route to retrieve patient details using fingerprint for emergency cases
@app.route('/emergency_lookup', methods=['POST'])
def emergency_lookup():
    data = request.get_json()
    fingerprint = data['fingerprint']
    
    # Lookup in Hospital B's database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE fingerprint = ?", (fingerprint,))
    patient = cursor.fetchone()
    
    if patient:
        conn.close()
        return jsonify({'patient_id': patient['patient_id'], 
                        'name': patient['name'], 
                        'age': patient['age'], 
                        'gender': patient['gender'], 
                        'allergy': patient['allergy'], 
                        'symptoms': patient['symptoms']})
    else:
        # If not found in Hospital B, check Hospital A
        response = requests.post("http://127.0.0.1:5001/emergency_lookup", json={'fingerprint': fingerprint})
        hospital_a_data = response.json()
        conn.close()
        return jsonify(hospital_a_data)

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Running on port 5002 for Hospital B
