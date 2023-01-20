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
from datetime import date
import pyodbc
from email.message import EmailMessage
import ssl
import smtplib

# Connect to database
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=H4K4MSPC\SQLEXPRESS;'
                      'Database=DIABETES;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor() 
    
# -----------------------------------train model----------------------------------- #
# Read dataset
diabetes_dataset = pd.read_csv(r"D:\Documents(D)\Git\DiabetsDisease\diabetes\diabetes.csv")

# Separating the data and labels
X = diabetes_dataset.drop(columns = 'Outcome', axis=1)
Y = diabetes_dataset['Outcome']

# Standardization Data
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
# -----------------------------------train model----------------------------------- #

# ------------------------------- Web page ------------------------------------ #
# page title
st.title('Diyabet Hastalığı Tespit Sistemi')

# Getting Ad Soyad E-mail from the user
col1, col2, col3 = st.columns(3)

with col1:
    Ad = st.text_input('Ad*')
    
with col2:
    Soyad = st.text_input('Soyad*')

with col3:
    Eposta = st.text_input('E-posta*')

st.header("Diyabet Test Bilgileri")

# Getting Diyabet Test Bilgileri
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

diab_diagnosis = ''

# Checkbok => Button will apear when checkbox is checked
agree = st.checkbox('Bilgilerimin işlenmesini onaylıyorum. (Girilen bilgiler üçüncü kişiler ile paylaşılmayacaktır.)')


# -------------------------Send Email fucntion------------------------- #
def SendEmail():
    email_sender = 'diabetespredictionn@gmail.com'
    email_password = 'uppcuyiimiujdjdj'
    email_receiver = str(Eposta)
    
    result = ""
    if prediction[0] == 0:
        result = "negatiftir"
    else:
        result = "Pozitifttir"
        
    subject = 'Diyabet Test Sonucu'
    body = """Sayın {0} {1} 
    {2} tarihinde yaptırmış olduğunuz diyabet testinizin sonucu {3}.
    Bize gönderdiğiniz tüm bilgiler:
        E-posta:{4}
        Gebelik Sayısı:{5}
        Glikoz Seviyesi:{6}
        Kan Basıncı:{7}
        Deri Kalınlığı:{8}
        Insulin Seviyesi:{9}
        Vücut Kitle Endeksi:{10}
        Diyabet Soyağacı:{11}
        Yaş:{12}
        
        Diyabet hastalığı hakkında bilgi almak için şu https://www.turkdiab.org/diyabet-hakkinda-hersey.asp?lang=TR&id=46 ulaşabilirsiniz
    """.format(Ad, Soyad, date.today(), result, Eposta, Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age)
    
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
# -------------------------Send Email fucntion------------------------- #

# ------------------------Test and Show Result------------------------ #
if agree:  
    # creating a button for Prediction
    if st.button('Test Sonucunu Görüntüleyin'):
        # If Ad Soyad E-mail textbox is no value Error message will show
        if Ad == "" and Soyad == "" and Eposta == "":
            diab_diagnosis = 'Gerekli alanları doldurun'
            st.error(diab_diagnosis)
        
        # Test and Show Result
        else:
            # Create list of input data to predict 
            diab_prediction = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
            
            # changing the input_data to numpy array
            input_data_as_numpy_array = np.asarray(diab_prediction)
    
            # reshape the array as we are predicting for one instance
            input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
            
            # standardize the input data
            std_data = scaler.transform(input_data_reshaped)
            
            # prediction
            prediction = classifier.predict(std_data)
        
            # --------- Showing result ---------------#
            # Diabetic
            if (prediction[0] == 1):
                # ---- show output ----#
                diab_diagnosis = 'Diyabet Hastasısınız'
                st.error(diab_diagnosis)
                # ---- show output ----#
                # send email
                SendEmail()
            # No diabetic
            else:
                # ---- show output ----#
                diab_diagnosis = 'Diyabet Hastası Değilsiniz'
                st.success(diab_diagnosis)
                # ---- show output ----#
                # send email
                SendEmail()
            # --------- Showing result ---------------#
            
            # ------Check the email if it is already in database------ #
            cursor.execute("SELECT eposta from Hasta where eposta=?",Eposta )
            eposta = cursor.fetchall()
            conn.commit()
            # if not add to database 
            if len(eposta) == 0:
                #Add Hasta to DB_TBL
                cursor.execute("EXEC HastaEkle @ad=?, @soyad=?, @eposta = ?",Ad,Soyad,Eposta)
                conn.commit()
            # ------Check the email if it is already in database------ #
            
            # get HastaID
            cursor.execute("SELECT HastaID from Hasta where eposta=?",Eposta )
            HastaID = cursor.fetchall()
            conn.commit()

            #Add Test bilgileri and result to DB_TBL
            params = (HastaID[0][0], Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, int(prediction[0]))
            cursor.execute("EXEC TestEkle @hastaID=?, @gebelik=?, @glikoz=?, @kan=?, @deri=?, @insulin=?, @vke=?, @soyagac=?, @yas=?, @sonuc=?",params )
            conn.commit()
        
# ------------------------Test and Show Result------------------------ #    
    

# ------------------------------- Web page ------------------------------------ #    
    
    
    
    
    
    
    
    
    
    
    
    
    