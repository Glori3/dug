import mysql.connector

# Database connection parameters
db_config = {
    'host': 'localhost',
    'user': 'root',  # Default XAMPP MySQL username
    'password': '',  # Default XAMPP MySQL password (blank by default)
    'database': 'drug_allergy_system'  # The name of the database you created
}

# Establish connection
connection = mysql.connector.connect(**db_config)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Example query to retrieve all patients
cursor.execute("SELECT * FROM patients")

# Fetch and print results
patients = cursor.fetchall()
for patient in patients:
    print(patient)

# Close the cursor and connection
cursor.close()
connection.close()
