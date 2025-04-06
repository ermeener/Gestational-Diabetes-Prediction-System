from flask import Flask, request, render_template, jsonify, redirect, url_for, session
import numpy as np
import pandas as pd
import joblib
import pickle

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "1279MohamedGtumb12"




loaded_model = pickle.load(open(r'C:\Users\LENOVO\Desktop\Gestational Diabetes Project\trained_model.sav', 'rb'))



print("Model loaded successfully!")

def diabetes_prediction(input_data):
    input_data_as_numpy = np.asarray(input_data, dtype=float)  # Convert inputs to float
    input_data_reshaped = input_data_as_numpy.reshape(1, -1)
    prediction = loaded_model.predict(input_data_reshaped)
    return 'The person is not diabetic' if prediction[0] == 0 else 'The person is diabetic'


# Load datasets
sym_des = pd.read_csv(r"data/Diabetes_Severity_Data.csv")
description = pd.read_csv(r"data/description.csv")
medications = pd.read_csv(r'data/diabetes_medications.csv')

# Load diet plan data
diet_df = pd.read_csv(r"data\diet.csv")

def get_diet_plan():
    """Returns the diet plan as a formatted string."""
    return "\n".join([f"{row['Food Category']}: {row['Examples']} ({row['Recommended Serving']})" for _, row in diet_df.iterrows()])


# # Helper function to retrieve disease details
# def helper(dis):
#     desc = description[description['Disease'] == dis]['Description']
#     desc=" ".join(desc)([w for w in desc])


#     med=medications[medications['Disease'] == dis]['Medication']
#     med=[med for med in med.values]
    
#     diet=diets[diets['Disease'] == dis]['Diet']
#     diet=[diet for diet in diet.values]

   

    return desc, med, diet

symptoms_dict = {
    'increased_thirst': 0,
    'frequent_urination': 1,
    'fatigue': 2,
    'blurred_vision': 3,
    'nausea': 4,
    'vomiting': 5,
    'weight_gain': 6,
    'excessive_hunger': 7,
    'sugar_in_urine': 8,
    'high_blood_sugar': 9,
    'slow_healing_wounds': 10,
    'dry_mouth': 11,
    'frequent_infections': 12,
    'dehydration': 13,
    'lethargy': 14,
    'dizziness': 15,
    'swollen_legs': 16,
    'preeclampsia_risk': 17,
    'high_blood_pressure': 18
}

# Dictionary mapping model output to disease names
diseases_list = {
    0: 'Gestational Diabetes - Mild',
    1: 'Gestational Diabetes - Moderate',
    2: 'Gestational Diabetes - Severe (requiring insulin therapy)',
    3: 'Preeclampsia (complication of gestational diabetes)'
}

# Model Prediction Function


@app.route("/")
def home():
    # Clear result on refresh if desired
    session.pop("result", None)
    session.pop("diet_plan", None)
    return render_template("index.html", result=None, diet_plan=None)

feature_names = [
    "Case Number", "Age", "No of Pregnancy", "Gestation in previous Pregnancy",
    "BMI", "HDL", "Family History", "unexplained prenetal loss", 
    "Large Child or Birth Default", "PCOS", "Sys BP", "Dia BP", "OGTT",
    "Hemoglobin", "Sedentary Lifestyle", "Prediabetes", "Outcome"
]

def to_bool(value):
    return 1 if value.lower() == "yes" else 0




@app.route("/predict", methods=["POST"])
def predict():
    data = request.form
    name = data.get('name', 'The patient')

    # Debugging: Print received data
    print("Received form data:", data)

    # Required fields except optional ones
    required_fields = [
        "age", "no_of_pregnancy", "previous_gestational_diabetes",
        "bmi", "family_history", "prenatal_loss", "large_child", "pcos",
        "sys_bp", "dia_bp", "sedentary_lifestyle", "prediabetes"
    ]

    # **🟡 Allow HDL, OGTT, Hemoglobin to be missing**
    optional_fields = ["hdl", "ogtt", "hemoglobin"]

    # Check for missing required fields
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        print("❌ Missing required fields:", missing_fields)
        return jsonify({"error": f"Missing field(s): {', '.join(missing_fields)}"}), 400
    
    try:
        # Convert data types
        age = int(data.get("age"))
        no_of_pregnancy = int(data.get("no_of_pregnancy"))
        previous_gdm = int(data.get("previous_gestational_diabetes"))
        bmi = float(data.get("bmi"))
        family_history = int(data.get("family_history"))

        # Convert "yes"/"no" to 1/0
        prenatal_loss = 1 if data.get("prenatal_loss", "").lower() == "yes" else 0
        large_child = 1 if data.get("large_child", "").lower() == "yes" else 0
        pcos = 1 if data.get("pcos", "").lower() == "yes" else 0

        sys_bp = int(data.get("sys_bp"))
        dia_bp = int(data.get("dia_bp"))
        sedentary_lifestyle = int(data.get("sedentary_lifestyle"))
        prediabetes = int(data.get("prediabetes"))

        # **🟡 Handle missing HDL, OGTT, Hemoglobin values**
        hdl = float(data.get("hdl", -1)) if data.get("hdl") else -1  # Default to -1 if missing
        hemoglobin = float(data.get("hemoglobin", -1)) if data.get("hemoglobin") else -1
        ogtt = data.get("ogtt", "").lower() if data.get("ogtt") else "unknown"

        # 🟢 **Validate OGTT Input (if provided)**
        valid_ogtt_values = ["normal", "impaired", "diabetic", "unknown"]
        if ogtt not in valid_ogtt_values:
            print(f"❌ ERROR: Unexpected OGTT value: {ogtt}")
            return jsonify({"error": f"Invalid OGTT value: {ogtt}. Expected values: {valid_ogtt_values}"}), 400

        # **🟢 Diabetes Risk Logic**
        if (
            ogtt == "diabetic" or
            bmi > 25 or
            sys_bp > 130 or
            dia_bp > 85 or
            previous_gdm == 1 or
            family_history == 1 or
            prenatal_loss == 1 or
            large_child == 1 or
            pcos == 1 or
            sedentary_lifestyle == 1 or
            prediabetes == 1 or
            (hemoglobin != -1 and hemoglobin < 12)  # Only check if hemoglobin was provided
        ):
            result = f"{name} is at risk of diabetes."
            diet_plan = get_diet_plan()
        else:
            result = f"{name} is not at risk of diabetes."
            diet_plan = None

        # Store result in session and render template
        session["result"] = result
        session["diet_plan"] = diet_plan
        return render_template("index.html", result=result, diet_plan=diet_plan)

    except ValueError as e:
        print(f"❌ ValueError: {e}")
        return jsonify({"error": f"Invalid input type: {str(e)}"}), 400

if __name__ == "__main__":
    app.run(debug=True)



    



  #dis_des=dis_desc,dis.med=dis_diet,  dis.med=dis_med)
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)
