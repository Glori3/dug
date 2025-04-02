<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "drug_allergy_system";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Insert data if form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $age = $_POST['age'];
    $gender = $_POST['gender'];
    $weight = $_POST['weight'];
    $height = $_POST['height'];
    $bmi = $_POST['bmi'];
    $chronic_conditions = $_POST['chronic_conditions'];
    $drug_allergies = $_POST['drug_allergies'];
    $genetic_disorders = $_POST['genetic_disorders'];
    $diagnosis = $_POST['diagnosis'];
    $symptoms = $_POST['symptoms'];
    $fingerprint_id = $_POST['fingerprint_id'];

    $sql = "INSERT INTO patients (Age, Gender, Weight_kg, Height_cm, BMI, Chronic_conditions, Drug_allergies, Genetic_Disorders, Diagnosis, Symptoms, Fingerprint_ID) 
            VALUES ('$age', '$gender', '$weight', '$height', '$bmi', '$chronic_conditions', '$drug_allergies', '$genetic_disorders', '$diagnosis', '$symptoms', '$fingerprint_id')";

    if ($conn->query($sql) === TRUE) {
        echo "New patient record inserted successfully!";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}

$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register Patient</title>
    <style>
        /* Center the content vertically and horizontally */
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            height: 150vh; /* Full height of the viewport */
            background-color: #f4f4f4;
            display: flex;
            justify-content:horizontally;
            align-items: horizontally; /* Vertically center the content */
        }
        .container {
            background-color: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 600px; /* Adjust the max width for form */
        }
        h2 {
            text-align: center;
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
        }
        form {
            display: block;
        }
        label {
            display: block;
            margin: 10px 0 5px;
            font-size: 16px;
            color: #333;
        }
        input, select {
            padding: 10px;
            font-size: 16px;
            border: 2px solid #ccc;
            border-radius: 4px;
            width: 100%;
            margin-bottom: 15px;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
            padding: 12px;
            width: 100%;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
        input[type="number"], input[type="text"], input[type="date"], select {
            width: 100%;
        }
    </style>
</head>
<body>

    <div class="container">
        <h2>Register New Patient</h2>
        <form method="post" action="">
            <label for="age">Age:</label>
            <input type="number" name="age" required placeholder="Enter age">

            <label for="gender">Gender:</label>
            <select name="gender" required>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
            </select>

            <label for="weight">Weight (kg):</label>
            <input type="number" step="0.1" name="weight" required placeholder="Enter weight">

            <label for="height">Height (cm):</label>
            <input type="number" step="0.1" name="height" required placeholder="Enter height">

            <label for="bmi">BMI:</label>
            <input type="number" step="0.1" name="bmi" required placeholder="Enter BMI">

            <label for="chronic_conditions">Chronic Conditions:</label>
            <input type="text" name="chronic_conditions" placeholder="Enter chronic conditions">

            <label for="drug_allergies">Drug Allergies:</label>
            <input type="text" name="drug_allergies" placeholder="Enter drug allergies">

            <label for="genetic_disorders">Genetic Disorders:</label>
            <input type="text" name="genetic_disorders" placeholder="Enter genetic disorders">

            <label for="diagnosis">Diagnosis:</label>
            <input type="text" name="diagnosis" placeholder="Enter diagnosis">

            <label for="symptoms">Symptoms:</label>
            <input type="text" name="symptoms" placeholder="Enter symptoms">

            <label for="fingerprint_id">Fingerprint ID:</label>
            <input type="text" name="fingerprint_id" required placeholder="Enter fingerprint ID">

            <input type="submit" value="Register Patient">
        </form>
    </div>

</body>
</html>
