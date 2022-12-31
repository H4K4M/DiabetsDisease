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


diabetes_dataset = pd.read_csv('D:\Documents(D)\Git\DiabetsDisease\diabetes\diabetes.csv')
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


# getting the input data from the user
col1, col2, col3 = st.columns(3)

with col1:
    Pregnancies = st.text_input('Ad')
    
with col2:
    Glucose = st.text_input('Soyad')

with col3:
    BloodPressure = st.text_input('E-posta')

    
st.header("Diyabet Test Bilgileri")
    
col1, col2, col3 = st.columns(3)
with col1:
    Pregnancies = st.number_input('Gebelik sayısı', min_value=0, max_value=20)
    
with col2:
    Glucose = st.number_input('Glikoz miktarı', min_value=0, max_value=200)

with col3:
    BloodPressure = st.number_input('Kan basıncı', min_value=0, max_value=150)

with col1:
    SkinThickness = st.number_input('Cilt kalınlığı değeri', min_value=0, max_value=100)

with col2:
    Insulin = st.number_input('İnsülin miktarı', min_value=0, max_value=1000)

with col3:
    BMI = st.number_input('BMI (Vücut kitle indeksi)', min_value=0, max_value=80)

with col1:
    DiabetesPedigreeFunction = st.number_input('Diyabet soyağacı fonksiyonu', min_value=0, max_value=3)

with col2:
    Age = st.number_input('Yaş', min_value=0, max_value=110)


# code for Prediction
diab_diagnosis = ''

agree = st.checkbox('Bilgilerimin işlenmesini onaylıyorum. (Girilen bilgiler üçüncü kişiler ile paylaşılmayacaktır.)')

if agree:
    
    # creating a button for Prediction
    if st.button('Test Sonucunu Görüntüleyin'):
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
            diab_diagnosis = 'Diyabet Hastasısınız'
            st.error(diab_diagnosis)
        else:
            diab_diagnosis = 'Şeker Hastası Değilsiniz'
            st.success(diab_diagnosis)
      
      
        input_list = diab_prediction
        input_list.append(prediction[0])


    # Open file in append mode
        with open('diabetes.csv', 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(input_list)
    
    
    

else:
    diab_diagnosis = 'Gerekli alanları doldurun'