# Gestational-Diabetes-Prediction-System

 This is a machine learning-powered web application that predicts the risk of Gestational Diabetes Mellitus (GDM) in pregnant women. This tool is designed to assist healthcare workers and pregnant individuals by providing early warnings and promoting informed medical follow-ups.

## 🩺 About the Project

This project was developed as part of my final year research to provide an accessible, supportive digital health tool for maternal care — especially in underserved communities. 
---

Using a Random Forest model, grid search optimization, and a simple Flask web app, this tool takes in basic health metrics and returns a prediction for gestational diabetes risk. If a person is found at risk, the web-app also provides a gentle push in the form of diet recommendations.

---

## 🧭 Purpose Behind the Project

I built this project with people in mind who may **not have regular access to medical facilities**, prenatal screenings, or early diagnostics. It’s not meant to replace doctors or medical professionals — it's a **support tool**. A simple, lightweight web app that might help someone take the first step toward seeking care.

Health tech should **support**, not replace, healthcare. This is one example of how AI can be applied responsibly, especially in underserved communities.

---

## 🔍 What It Does

- 🧼 Cleans and explores medical data (EDA)
- 🤖 Builds a Random Forest classifier 
- 📈 Evaluates performance (accuracy, precision, recall, F1-score)
- 💾 Saves the trained model using `pickle`
- 🌐 Deploys a clean interface using Flask + Bootstrap

You can enter basic metrics like glucose, BMI, age, etc., and get a live prediction through the browser.

---

## 🧠 Why I Built It

As a final-year BSc Software Development student, I wanted to move beyond class exercises and build something that *actually solves a real problem*. Gestational diabetes is under-discussed, particularly in Africa and other low-resource regions, yet it’s a serious maternal health risk.

This app reflects my growing interest in:
- **Machine learning for healthcare**
- **Socially responsible AI**
- **Accessible diagnostics in underrepresented regions**

## 🛠 Tools Used

- Python (pandas, scikit-learn, matplotlib, seaborn)
- Jupyter Notebook for analysis + training
- Flask for web deployment
- HTML + Bootstrap for the frontend
