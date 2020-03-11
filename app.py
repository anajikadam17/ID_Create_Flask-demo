# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 12:40:42 2020

@author: Anaji
"""

import pandas as pd
import numpy as np
import re
from flask import Flask, request, jsonify, render_template, url_for, Response
import pickle
import pymysql
import io
import csv
from flaskext.mysql import MySQL
import io
import xlwt
import pymysql
import mysql

app = Flask(__name__)
# Connect to the database
connection = pymysql.connect(host='localhost',
                         user='root',
                         password='',
                         db='flask_demo')
# create cursor
cursor=connection.cursor()
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'flask_demo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



global df
@app.route('/')
def index():
    #message = "ML Shop"
    return render_template('index.html')

@app.route("/Task1")
def Task1():
  return render_template("Task1.html")

    
@app.route('/idcreate',methods=['POST'])
def idcreate():
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)  
        filename1 = f.filename
    df = pd.read_excel(filename1)
    
    
    def ID(df):
        def clean(df):
            df['Name'] = df['Name'].apply(lambda x: str(x).upper())
            df['Mobile_Number'] = df['Mobile_Number'].apply(lambda x: re.sub('[^0-9]+','',str(x)))  # Remove character and special character
            df['X5'] = df['Mobile_Number'].apply(lambda x: len(str(x)))                  # After remove character length of number
            return df
    
        def len20n10(df):                                                   # function for len 10 and 20 create dataframe for that                                   
            f = df[df['X5']==10]
            b = df[df['X5']==20]
            b = pd.DataFrame(np.repeat(b.values,2,axis=0),columns=b.columns)
            for i in range(0,len(b)):
                if i%2==1:
                    b['Mobile_Number'][i]=b['Mobile_Number'][i][10:]
                else:
                    b['Mobile_Number'][i]=b['Mobile_Number'][i][:10]
            b =  b.append(f, ignore_index=True)
            return b
        
        def len30n40(df):                                                   # function for len 10 and 20 create dataframe for that                                   
            x = df[df['X5']==30]
            x = pd.DataFrame(np.repeat(x.values,3,axis=0),columns=x.columns)
            for i in range(0,len(x)):
                if i%3==0:
                    x['Mobile_Number'][i]=x['Mobile_Number'][i][:10]
                elif i%3==1:
                    x['Mobile_Number'][i]=x['Mobile_Number'][i][10:20]
                elif i%3==2:
                    x['Mobile_Number'][i]=x['Mobile_Number'][i][-10:]
    
            y = df[df['X5']==40]
            y = pd.DataFrame(np.repeat(y.values,4,axis=0),columns=y.columns)
            for i in range(0,len(y)):
                if i%4==0:
                    y['Mobile_Number'][i]=y['Mobile_Number'][i][:10]
                elif i%4==1:
                    y['Mobile_Number'][i]=y['Mobile_Number'][i][10:20]
                elif i%4==2:
                    y['Mobile_Number'][i]=y['Mobile_Number'][i][20:30]
                elif i%4==3:
                    y['Mobile_Number'][i]=y['Mobile_Number'][i][-10:]
            y =  x.append(y, ignore_index=True)
            return y
    
        def mixlen(df):
            def checkNo(x):
                if (len(x)==8)|(len(x)==6):
                    return 'LN'
                else:
                    return ''
    
            def checkNo11to19(x):
                x = x[:10]
                pattern=re.compile("^[9876]")
                match=re.match(pattern,x)
                if match:
                    return x
                else:
                    return ''
            def checkNo21(x):
                x = x[:10]
                x1 = x[11:]
                pattern=re.compile("^[9876]")
                match=re.match(pattern,x)
                if match:
                    return x
                else:
                    return ''
    
                pattern=re.compile("^[9876]")
                match=re.match(pattern,x1)
                if match:
                    return x1
                else:
                    return ''
    
    
            e = (df['X5']<10)|(df['X5']==11)|(df['X5']==12)|(df['X5']==18)|(df['X5']==19)|(df['X5']==21)|(df['X5']==22)
            df2 = df[e]
            df2['X6'] = df2['Mobile_Number'].apply(lambda x: checkNo(x) if (len(x)<10) else '')
            df2['X7'] = df2['Mobile_Number'].apply(lambda x: checkNo11to19(x) if (len(x)==11)|(len(x)==12)|(len(x)==18)|(len(x)==19) else '')
            df2['X8'] = df2['Mobile_Number'].apply(lambda x: checkNo21(x) if len(x)==21 else '')
            df2['X4'] = df2['X7']+df2['X8']
            df2['X5'] = df2['Mobile_Number'].apply(lambda x: len(str(x)))
            df3 = df2[['Name','X4','X5']]
            return df3
    
        df = clean(df)
        b = len20n10(df)
        y = len30n40(df)
        b = b.append(y, ignore_index=True) 
        d = mixlen(df)
        df =  b.append(d, ignore_index=True)        # final dataframe 
        df['Mobile_Number'] = df['Mobile_Number'].apply(lambda x: '' if type(x)==float else x)
        
        df['ID'] = [i for i in range(1, df.shape[0]+1)]   # default id base on Index
        df['ID1'] = df.groupby(['Name'])['ID'].rank(method = 'first', ascending = True).astype(int)  # Id based on Name 
        df['ID2'] = df.groupby(['Mobile_Number'])['ID'].rank(method = 'first', ascending = True).astype(int) # Id based on mobile number
        df['ID'] = df['ID'].astype(str)+'.'+df['ID2'].astype(str)+'.'+df['ID1'].astype(str)
        # id format is ID + Mobile ID + Name ID
        col = ['ID','Name', 'Mobile_Number']
        df = df[col]
        return df
    
    df = ID(df)
    # creating column list for insertion
    cols = "`,`".join([str(i) for i in df.columns.tolist()])
    # Insert DataFrame recrds one by one.
    for i,row in df.iterrows():
        sql = "INSERT INTO `id` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
        cursor.execute(sql, tuple(row))
    # the connection is not autocommitted by default, so we must commit to save our changes
    connection.commit()
    data1 = df.to_html()
    #write html to file 
    text_file = open("data1.html", "w") 
    text_file.write(data1) 
    text_file.close()
    
    return render_template("success.html")  
  
@app.route('/download')
def download():
    return render_template('download.html')
@app.route('/download/report/excel')
def download_report():
 conn = None
 cursor = None
 try:
  conn = mysql.connect()
  cursor = conn.cursor(pymysql.cursors.DictCursor)
  
  cursor.execute("SELECT * FROM id")
  result = cursor.fetchall()
  
  #output in bytes
  output = io.BytesIO()
  #create WorkBook object
  workbook = xlwt.Workbook()
  #add a sheet
  sh = workbook.add_sheet('Data Report')
  
  #add headers
  sh.write(0, 0, 'ID')
  sh.write(0, 1, 'Name')
  sh.write(0, 2, 'Mobile_Number')
  
  idx = 0
  for row in result:
   sh.write(idx+1, 0, str(row['ID']))
   sh.write(idx+1, 1, row['Name'])
   sh.write(idx+1, 2, row['Mobile_Number'])
   idx += 1
  
  workbook.save(output)
  output.seek(0)
  cursor.execute("TRUNCATE id;")   # Truncate id table
  return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=ID_report.xls"})
  
 except Exception as e:
  print(e)
 finally:
  cursor.close() 
  conn.close()
  

if __name__ == "__main__":
    app.run(debug=True)