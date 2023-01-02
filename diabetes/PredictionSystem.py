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
from datetime import date
import pyodbc 
import smtplib, ssl

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=H4K4MSPC\SQLEXPRESS;'
                      'Database=Diabetes_DB;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor() 
    


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


# getting the input data from the user
col1, col2, col3 = st.columns(3)

with col1:
    Ad = st.text_input('Ad')
    
with col2:
    Soyad = st.text_input('Soyad')

with col3:
    Eposta = st.text_input('E-posta')

    
st.header("Diyabet Test Bilgileri")
    
col1, col2, col3 = st.columns(3)
with col1:
    Pregnancies = st.number_input('Gebelik sayısı', min_value=0, max_value=20)
    
with col2:
    Glucose = float(st.number_input('Glikoz miktarı', min_value=0, max_value=200))

with col3:
    BloodPressure = float(st.number_input('Kan basıncı', min_value=0, max_value=150))

with col1:
    SkinThickness = float(st.number_input('Cilt kalınlığı değeri', min_value=0, max_value=100))

with col2:
    Insulin = float(st.number_input('İnsülin miktarı', min_value=0, max_value=1000))

with col3:
    BMI = float(st.number_input('BMI (Vücut kitle indeksi)', min_value=0, max_value=80))

with col1:
    DiabetesPedigreeFunction = float(st.number_input('Diyabet soyağacı fonksiyonu', min_value=0, max_value=3))

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
        
        cursor.execute("SELECT eposta from Hasta where eposta=?",Eposta )
        eposta = cursor.fetchall()
        conn.commit()
        
        if len(eposta) == 0:
            #Add Hasta to DB_TBL
            cursor.execute("EXEC HastaEkle @ad=?, @soyad=?, @eposta = ?",Ad,Soyad,Eposta)
            conn.commit()
        
        cursor.execute("SELECT HastaID from Hasta where eposta=?",Eposta )
        HastaID = cursor.fetchall()
        conn.commit()
        
        HastaID = HastaID[0][0]
        result = int(prediction[0])
        date = date.today()
        #Add Hasta to DB_TBL
        params = (HastaID, Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, str(date), result)
        cursor.execute("EXEC TestEkle @hastaID=?, @gebelik=?, @glikoz=?, @kan=?, @deri=?, @insulin=?, @vke=?, @soyagac=?, @yas=?, @tarih=?, @sonuc=?",params )
        conn.commit()
        
        
        # Sending Email
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "diabetespredictionn@gmail.com"  # Enter your address
        receiver_email = Eposta  # Enter receiver address
        password = "diyabet1234@"
        
        
        cursor.execute("EXEC HastaTestGetir @eposta = ?",Eposta)
        GetData  = cursor.fetchall()
        conn.commit()
        TestID = GetData[-1][0]
        Name = GetData[-1][1]
        date = GetData[-1][2]
        TestResult = ""
        if GetData[-1][-1] == 1:           
            TestResult = "Pozitiftir."
        else:
            TestResult = "negatiftir."
        
        message = "Sayın " + str(Name) +", "+ str(date) + " tarihinde yaptırmış olduğunuz "+ str(TestID) + " numaralı son testin sonucu "+str(TestResult)
        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        
        
        

    # Open file in append mode
        with open('diabetes.csv', 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(input_list)
    
    
    

else:
    diab_diagnosis = 'Gerekli alanları doldurun'