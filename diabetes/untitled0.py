# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 13:15:55 2023

@author: ha-ka
"""

import pyodbc 

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=H4K4MSPC\SQLEXPRESS;'
                      'Database=DIABETES;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor() 


Ad = "sgfdg"
Soyad = "dafsd"
Eposta = "adsafere"

# cursor.execute("INSERT INTO Hasta (Ad, Soyad, Eposta) VALUES(?,?,?)",(Ad,Soyad,Eposta))
# conn.commit()

cursor.execute("EXEC HastaEkle @ad=?, @soyad=?, @eposta = ?",Ad,Soyad,Eposta)
conn.commit()