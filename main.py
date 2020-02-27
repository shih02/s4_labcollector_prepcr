from flask import Flask, render_template, request
import requests
import re
import H
import json
from openpyxl import load_workbook, workbook

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/result", methods=["POST"])
def result():
    samplelist = ""
    dict_list = []
    name = request.form.get("name") #this is for searching
    wb = load_workbook(filename = name)
    ws = wb['Sheet1']

    for x in range(1, ws.max_row+1):
        id = ws.cell(row = x, column = 1).value
        samplelist = samplelist + id +","

    #generate response and set response variables 
    # // careful with this loop as it can break LC server!!
    url = H.url_v2 + samplelist
    response = requests.request("GET", url, headers=H.headers)
    response_text = response.text.replace("'",'"')
    my_response = json.loads(response_text)
    # //

    #rebuild response text to set count:lab id:volume
    sample = samplelist.split(",")
    for i in range(x):
        dict_list.append(dict(ID=sample[i], conc=my_response[i]['volume'], num=i+1))
          
    return render_template("result.html", dict_list=dict_list)
    
@app.route("/update", methods=["POST"])
def update():
    
    name = request.form.get("name") #this is for searching
    wb = load_workbook(filename = name)
    ws = wb['Sheet1']
    samplelist = ""
    dict_list = []

    for x in range(1, ws.max_row+1):
        id = ws.cell(row = x, column = 1).value
        samplelist = samplelist + id +","
    #generate response and set response variables 
    # // careful with this loop as it can break LC server!!
    url = H.url_v2 + samplelist
    response = requests.request("GET", url, headers=H.headers)
    response_text = response.text.replace("'",'"')
    my_response = json.loads(response_text)
    # //

    for x in range(1, ws.max_row+1):
        id = ws.cell(row = x, column = 1).value
        concentration = ws.cell(row = x, column = 2).value
        if id == my_response[x-1]['label']:
            payload = {'comments': 'VS dictionary testing' + str(x),'origin': concentration,'volume': concentration}
            put_response = requests.request("PUT", H.put_url+my_response[x-1]['count'], headers=H.headers, data = payload)
            dict_list.append(dict(ID=id, conc=concentration,num=x)) #count was excluded in dict_list

    return render_template("update.html", dict_list=dict_list)
    
if __name__ == "__main__":
    app.run(debug=True, port="5000")