# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 13:15:55 2023

@author: ha-ka
"""

import pyodbc 
from datetime import date
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=H4K4MSPC\SQLEXPRESS;'
                      'Database=DIABETES;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor() 


# Ad = str(input("Ad: "))
# Soyad = str(input("Soyad: "))
# Eposta = str(input("E-posta: "))

# # cursor.execute("INSERT INTO Hasta (Ad, Soyad, Eposta) VALUES(?,?,?)",(Ad,Soyad,Eposta))
# # conn.commit()
# print()
# cursor.execute("EXEC HastaEkle @ad=?, @soyad=?, @eposta = ?",Ad,Soyad,Eposta)
# conn.commit()

cursor.execute("SELECT HastaID from Hasta where eposta='asdas'" )
HastaID = cursor.fetchall()
conn.commit()
HastaID = HastaID[0][0]
# print(HastaID[0][0])
# print(type(HastaID[0][0]))
date = date.today()
Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, date, result = 0,15,100,10,50,30,1.2,30,str(date),1
params = (HastaID, Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, date, result)
cursor.execute("EXEC TestEkle @hastaID=?, @gebelik=?, @glikoz=?, @kan=?, @deri=?, @insulin=?, @vke=?, @soyagac=?, @yas=?, @tarih=?, @sonuc=?",params )
conn.commit()