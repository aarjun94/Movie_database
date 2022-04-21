# def table():
#     data=[]
#     url = "https://en.wikipedia.org/wiki/Timothée Chalamet"
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     table=soup.find('table',{'class':'infobox biography vcard'})
#     rows=table.find_all('tr')
#     for row in rows:
#             data.append([cell.text.replace('\n', '')for cell in row.find_all(['th', 'td'])])

#     # print(data)
#     df = pd.DataFrame(data[2:9])

#     return df.to_html(header="False", table_id="table")

 
# @app.route('/health_insurance/', methods = ['POST', 'GET'])
# def health_insurance():
#     global poverty_data
#     if request.method == 'GET':
#         return f"The URL /data is accessed directly. Try going to '/form' to submit form"
#     if request.method == 'POST':
#         poverty_data = request.form
#         return render_template('health_insurance.html')


# @app.route('/earnings/', methods = ['POST', 'GET'])
# def earnings():
#     global health_ins_data
#     if request.method == 'GET':
#         return f"The URL /data is accessed directly. Try going to '/form' to submit form"
#     if request.method == 'POST':
#         health_ins_data = request.form
#         return render_template('earnings.html')

# @app.route('/data/', methods = ['POST', 'GET'])
# def data():
#     global earnings_data
#     if request.method == 'GET':
#         return f"The URL /data is accessed directly. Try going to '/form' to submit form"
#     if request.method == 'POST':
#         earnings_data = request.form
#         d4 = {}
#         d4.update(poverty_data)
#         d4.update(health_ins_data)
#         d4.update(earnings_data)

#         return render_template('data.html', form_data=d4)
 