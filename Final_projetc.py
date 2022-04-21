from flask import Flask,render_template,request
from Main import actor_profile
import pandas as pd
import requests
from bs4 import BeautifulSoup
 


app = Flask(__name__)
 
@app.route('/')
def index():
    return render_template('language.html')


 
if __name__ == '__main__':
    app.run(debug=True)

# table()

