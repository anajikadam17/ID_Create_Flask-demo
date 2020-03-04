# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 20:12:43 2020

@author: Anaji
"""

from app import app
from flask import Flask, send_file, render_template
 

app = Flask(__name__)

@app.route('/')
def upload_form():
 return render_template('download.html')

@app.route('/download')
def download_file():
 #path = "html2pdf.pdf"
 #path = "info.xlsx"
 path = "data.xlsx"
 #path = "sample.txt"
 return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
    
    
    
 <!--a href="{{ url_for('download_file') }}">Download</a> -->
 
 
 <p>
 <a href="{{ url_for('.download_file') }}">Download</a>
</p>