# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 12:40:42 2020

@author: Anaji
"""

import pandas as pd
import numpy as np
import re
from flask import Flask, request, jsonify, render_template
import pickle


app = Flask(__name__)

@app.route('/')
def index():
    #message = "ML Shop"
    return render_template('index.html')

@app.route("/Task1")
def Task1():
  return render_template("Task1.html")

@app.route('/idcreate',methods=['POST'])
def idcreate():
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
    
        def mob(x):
                pattern=re.compile("^[9876]")
                match=re.match(pattern,x)
                if match:
                    return x
                else:
                    return ''
    
        def mixlen(df):                                                      # function for len mix len create dataframe for that
            # Length of mobile number is not 10 and 20
            e = (df['X5']==21)  | (df['X5']==18) | (df['X5']<10)
            df2 = df[e]
            # if any mobile number having length less than 10 that is invalid no. IVN
            # landline number contain 8 digit number and 3 digit std code starting with 0
            # if landline no. other than 11 digit that is IVN
            def checkNo(x):
                return 'IVN'
            def checkNo18(x):
                return x[:10]
            def checkNo21(x):   # only if mobile number is present first in 21 digit
                a = x[:10]
                mob(a)
                b = x[11:]
                mob(b)
            # dt_new['MOBILE NUMBER'] =dt_new['MOBILE NUMBER'].fillna(0).apply(np.int64)
    
            df2['X6'] = df2['Mobile_Number'].apply(lambda x: checkNo(x) if len(x)<10 else '')
            df2['X7'] = df2['Mobile_Number'].apply(lambda x: checkNo18(x) if len(x)==18 else '')
            df2['X8'] = df2['Mobile_Number'].apply(lambda x: checkNo21(x) if len(x)==21 else '')
            df2['X4'] = df2['X7']+df2['X8']
            df2['X5'] = df2['Mobile_Number'].apply(lambda x: len(str(x)))
            # df2['X4'] =df2['X4'].fillna(0).apply(np.int64)
            df3 = df2[['Name','Mobile_Number','X5']]
            return df3
    
    
        df = clean(df)
        b = len20n10(df)
        d = mixlen(df)
        df =  b.append(d, ignore_index=True)        # final dataframe 
        df['Mobile_Number'] = df['Mobile_Number'].apply(lambda x: mob(str(x)))
    
        df['ID'] = [i for i in range(1, df.shape[0]+1)]   # default id base on Index
        df['ID1'] = df.groupby(['Name'])['ID'].rank(method = 'first', ascending = True).astype(int)  # Id based on Name 
        df['ID2'] = df.groupby(['Mobile_Number'])['ID'].rank(method = 'first', ascending = True).astype(int) # Id based on mobile number
        df['ID'] = df['ID'].astype(str)+'.'+df['ID2'].astype(str)+'.'+df['ID1'].astype(str)
        # id format is ID + Mobile ID + Name ID
        col = ['ID','Name', 'Mobile_Number']
        df = df[col]
        return df
    
    df = pd.read_excel('data.xlsx')
    df = ID(df)
    data1 = df.to_html()
    #write html to file 
    text_file = open("data1.html", "w") 
    text_file.write(data1) 
    text_file.close()
    
    #df.to_excel (r'data1.xlsx', index = None, header=True)
    #return render_template('index.html', prediction_text='Employee Salary should be $ {}'.format(output))
    return render_template("result.html") 
   
    #return render_template("result.html", prediction = df.to_html(titles = ['na', 'Female surfers', 'Male surfers'])) 
    #return render_template('result.html',tables=[df.to_html(), df.to_html(classes='male')],
   # titles = ['na', 'Female surfers', 'Male surfers'])

if __name__ == "__main__":
    app.run(debug=True)