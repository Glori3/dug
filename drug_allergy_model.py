import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load the dataset from the CSV file
df = pd.read_csv("drug_allergy_data.csv")  # Ensure correct path

# Initialize label encoders for categorical columns
label_encoder = LabelEncoder()

# Encode 'Gender' as example (Male = 0, Female = 1)
df['Gender'] = label_encoder.fit_transform(df['Gender'])

# Encode other categorical columns
df['Chronic_Conditions'] = label_encoder.fit_transform(df['Chronic_Conditions'].astype(str))
df['Drug_Allergies'] = label_encoder.fit_transform(df['Drug_Allergies'].astype(str))
df['Genetic_Disorders'] = label_encoder.fit_transform(df['Genetic_Disorders'].astype(str))
df['Diagnosis'] = label_encoder.fit_transform(df['Diagnosis'].astype(str))
df['Symptoms'] = label_encoder.fit_transform(df['Symptoms'].astype(str))
df['Recommended_Medication'] = label_encoder.fit_transform(df['Recommended_Medication'].astype(str))

# Convert 'Dosage' to numeric by extracting the numbers and ignoring the units (e.g., '400 mg' -> 400)
df['Dosage'] = df['Dosage'].str.extract('(\d+)', expand=False)
df['Dosage'] = pd.to_numeric(df['Dosage'], errors='coerce')  # Convert to numeric, NaN for invalid entries

# Convert 'Duration' to numeric by extracting the numbers and ignoring the units (e.g., '30 days' -> 30)
df['Duration'] = df['Duration'].str.extract('(\d+)', expand=False)
df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce')  # Convert to numeric, NaN for invalid entries

# Fill missing values for any other columns as needed
df = df.fillna(0)

# Drop non-numeric columns like Patient_ID
df = df.drop(columns=['Patient_ID'])

# Select the features (make sure these are numeric or encoded)
X = df.drop(columns=['Adverse_Reactions', 'Treatment_Effectiveness'])  # Assuming these are the target variables
y = df['Adverse_Reactions']  # Assuming this is the target

# Now proceed with model training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Model performance
print(f'Model accuracy: {model.score(X_test, y_test)}')
