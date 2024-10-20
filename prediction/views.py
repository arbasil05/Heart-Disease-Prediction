from django.shortcuts import render
import pandas as pd
import numpy as np


    

from django.shortcuts import render
import pandas as pd
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

def Home(request):
    return render(request,'Home.html')

def back(request):
    return render(request,'Home.html')

def preditcion(request):
    if request.method == 'POST':
        Age = float(request.POST.get('age'))
        Sex = request.POST.get('sex')
        Chest_pain_type = request.POST.get('cp')
        Rest_B_P = float(request.POST.get('trestbps'))
        Cholesterol = float(request.POST.get('chol'))
        Fasting_B_P = float(request.POST.get('fbs'))
        Max_Heart_Rate = float(request.POST.get('thalach'))
        Excersie_Induced_Angine = request.POST.get('exang')

        Sex_encoded = 1 if Sex.lower() == 'male' else 0
        cp_dict = {'typical': 1, 'atypical': 2, 'non-anginal': 3, 'asymptomatic': 4}
        Chest_pain_type_encoded = cp_dict.get(Chest_pain_type.lower(), 0)
        Excersie_Induced_Angine_encoded = 1 if Excersie_Induced_Angine.lower() == 'yes' else 0

        input_data = [Age, Sex_encoded, Chest_pain_type_encoded, Rest_B_P, Cholesterol, Fasting_B_P, Max_Heart_Rate, Excersie_Induced_Angine_encoded]

        df = pd.read_csv(r"C:\Users\arbas\OneDrive\Desktop\IBM Z Datathon\Heart_Disease_Prediction.csv")
        df['Heart Disease'] = df['Heart Disease'].map({'Absence': 0, 'Presence': 1})

        X = df.drop(columns=['Heart Disease', 'EKG results', 'ST depression', 'Slope of ST', 'Number of vessels fluro', 'Thallium'])
        y = df['Heart Disease']

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        model = LogisticRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)

        input_data_scaled = scaler.transform([input_data])  
        new_pred = model.predict(input_data_scaled)
        prediction_result = "Presence of heart disease" if new_pred[0] == 1 else "Absence of heart disease"
        return render(request, 'result.html', {'prediction_result': prediction_result})

