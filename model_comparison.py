# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix

# Load your dataset (replace with your actual dataset)
df = pd.read_csv('drug_allergy_data.csv')

# Drop the non-numeric or identifier column (e.g., Patient_ID if it's not relevant for prediction)
df = df.drop(columns=['Patient_ID'])  # Modify this based on your actual dataset

# Encode categorical columns (assuming you have categorical data)
# For non-numeric columns like 'Gender', 'Treatment_Effectiveness', etc., encode them to numeric values.
label_columns = ['Treatment_Effectiveness', 'Diagnosis', 'Chronic_Conditions', 'Drug_Allergies', 'Gender']
for col in label_columns:
    df[col] = LabelEncoder().fit_transform(df[col].astype(str))

# Split dataset into features and target
X = df.drop(columns=['Treatment_Effectiveness'])  # Adjust target column
y = df['Treatment_Effectiveness']

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 1: Apply SMOTE for class imbalance
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# Step 2: Feature scaling (if necessary for models like SVM)
scaler = StandardScaler()
X_train_res = scaler.fit_transform(X_train_res)
X_test = scaler.transform(X_test)

# Step 3: Hyperparameter Tuning (Using GridSearchCV)

# Define models for GridSearch
rf_model = RandomForestClassifier(random_state=42)
svm_model = SVC(random_state=42, probability=True)
xgb_model = XGBClassifier(random_state=42)

# Define parameter grids for GridSearchCV
rf_param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
svm_param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'rbf']
}
xgb_param_grid = {
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 7],
    'n_estimators': [50, 100, 200]
}

# Perform GridSearchCV for RandomForest
rf_grid_search = GridSearchCV(estimator=rf_model, param_grid=rf_param_grid, cv=3, n_jobs=-1, verbose=2)
rf_grid_search.fit(X_train_res, y_train_res)
print("Random Forest Best Parameters:", rf_grid_search.best_params_)
print("Random Forest Best Accuracy:", rf_grid_search.best_score_)

# Perform GridSearchCV for SVM
svm_grid_search = GridSearchCV(estimator=svm_model, param_grid=svm_param_grid, cv=3, n_jobs=-1, verbose=2)
svm_grid_search.fit(X_train_res, y_train_res)
print("SVM Best Parameters:", svm_grid_search.best_params_)
print("SVM Best Accuracy:", svm_grid_search.best_score_)

# Perform GridSearchCV for XGBoost
xgb_grid_search = GridSearchCV(estimator=xgb_model, param_grid=xgb_param_grid, cv=3, n_jobs=-1, verbose=2)
xgb_grid_search.fit(X_train_res, y_train_res)
print("XGBoost Best Parameters:", xgb_grid_search.best_params_)
print("XGBoost Best Accuracy:", xgb_grid_search.best_score_)

# Step 4: Cross-validation for robust evaluation
cv_scores_rf = cross_val_score(rf_grid_search.best_estimator_, X_train_res, y_train_res, cv=5, scoring='accuracy')
cv_scores_svm = cross_val_score(svm_grid_search.best_estimator_, X_train_res, y_train_res, cv=5, scoring='accuracy')
cv_scores_xgb = cross_val_score(xgb_grid_search.best_estimator_, X_train_res, y_train_res, cv=5, scoring='accuracy')

print("Cross-validation Accuracy (Random Forest):", cv_scores_rf.mean())
print("Cross-validation Accuracy (SVM):", cv_scores_svm.mean())
print("Cross-validation Accuracy (XGBoost):", cv_scores_xgb.mean())

# Step 5: Ensemble Method - Voting Classifier (combine models)
voting_clf = VotingClassifier(estimators=[
    ('rf', rf_grid_search.best_estimator_),
    ('svm', svm_grid_search.best_estimator_),
    ('xgb', xgb_grid_search.best_estimator_)
], voting='soft')

# Train the Voting Classifier
voting_clf.fit(X_train_res, y_train_res)

# Step 6: Model Evaluation - Classification Report and Confusion Matrix
y_pred = voting_clf.predict(X_test)

# Print Classification Report
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Plot Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
plt.matshow(cm, cmap='Blues', fignum=1)
plt.title("Confusion Matrix")
plt.colorbar()
plt.xlabel("Predicted")
plt.ylabel("True")
plt.show()
