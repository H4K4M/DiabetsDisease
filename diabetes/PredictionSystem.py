# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 10:22:29 2022

@author: ha-ka
"""
import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from csv import writer


diabetes_dataset = pd.read_csv('D:\Documents(D)\diabetes\diabetes.csv')
# separating the data and labels
X = diabetes_dataset.drop(columns = 'Outcome', axis=1)
Y = diabetes_dataset['Outcome']

#Standardization Data
scaler = StandardScaler()
scaler.fit(X)
standardized_data = scaler.transform(X)
X = standardized_data
Y = diabetes_dataset['Outcome']

#Split train and test data  80:20
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.2, stratify=Y, random_state=2)
classifier = svm.SVC(kernel='linear')
#training the support vector Machine Classifier
classifier.fit(X_train, Y_train)



# page title
st.title('Diyabet Hastalığı Tespit Sistemi')


# getting the user information from the user
col1, col2, col3 = st.columns(3)

with col1:
    Pregnancies = st.text_input('Ad')
    
with col2:
    Glucose = st.text_input('Soyad')

with col3:
    BloodPressure = st.text_input('E-posta')

    
st.header("Diyabet test bilgileri")
 # getting the input data from the user
col1, col2, col3 = st.columns(3)
with col1:
    Pregnancies = st.text_input('Gebelik sayısı')
    
with col2:
    Glucose = st.text_input('Glikoz miktarı')

with col3:
    BloodPressure = st.text_input('Kan basıncı')

with col1:
    SkinThickness = st.text_input('Cilt kalınlığı değeri')

with col2:
    Insulin = st.text_input('İnsülin miktarı')

with col3:
    BMI = st.text_input('BMI (Vücut kitle indeksi)')

with col1:
    DiabetesPedigreeFunction = st.text_input('Diyabet soyağacı fonksiyonu')

with col2:
    Age = st.text_input('Yaş')


# code for Prediction
diab_diagnosis = ''

# creating a button for Prediction
if st.button('Diabetes Test Result'):
    #diab_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
    diab_prediction = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
    # changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(diab_prediction)

    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
    # standardize the input data
    std_data = scaler.transform(input_data_reshaped)
    prediction = classifier.predict(std_data)
    
    if (prediction[0] == 1):
      diab_diagnosis = 'şeker hastasısınız'
    else:
      diab_diagnosis = 'şeker hastası değilsiniz'
      
      
    input_list = diab_prediction
    input_list.append(prediction[0])


# Open file in append mode
    with open('diabetes.csv', 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(input_list)
    
st.success(diab_diagnosis)
