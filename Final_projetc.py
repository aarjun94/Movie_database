from flask import Flask,render_template,request
 
poverty_data = {}
health_ins_data = {}
earnings_data = {}

app = Flask(__name__)
 
@app.route('/')
def index():
    return render_template('form.html')

 
@app.route('/health_insurance/', methods = ['POST', 'GET'])
def health_insurance():
    global poverty_data
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        poverty_data = request.form
        return render_template('health_insurance.html')


@app.route('/earnings/', methods = ['POST', 'GET'])
def earnings():
    global health_ins_data
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        health_ins_data = request.form
        return render_template('earnings.html')

@app.route('/data/', methods = ['POST', 'GET'])
def data():
    global earnings_data
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        earnings_data = request.form
        d4 = {}
        d4.update(poverty_data)
        d4.update(health_ins_data)
        d4.update(earnings_data)

        return render_template('data.html', form_data=d4)
 
 
app.run(host='localhost', port=5000)

