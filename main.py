from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import requests
import re
import H
import json
import os
from openpyxl import load_workbook, workbook

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/search', methods=["POST","GET"])
def result():
    if request.method == 'POST':
        samplelist = ""
        dict_list = []
        f = request.files['name']
        f.save(secure_filename(f.filename))        
        wb = load_workbook(filename = f)
        ws = wb.worksheets[0]

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
    else: 
        return render_template("search.html")

@app.route('/update', methods=["POST","GET"])
def update():
    if request.method == 'POST':
        samplelist = ""
        dict_list = []
        f = request.files['name']
        f.save(secure_filename(f.filename))        
        wb = load_workbook(filename = f)
        ws = wb.worksheets[0]

        for x in range(7, ws.max_row+1):
            id = ws.cell(row = x, column = 1).value
            if not ws.cell(row=x, colum = 9).value:
                ext = ws.cell(row=x, colum = 9).value
                if ext == "FE":
                    ext = "_10"
                elif ext == "SE":
                    ext = "_20"
                elif ext == "TE":
                    ext = "_30"
                elif ext == "FO":
                    ext = "_40"
            samplelist = samplelist + id + ext +","
        #generate response and set response variables 
        # // careful with this loop as it can break LC server!!
        url = H.url_v2 + samplelist
        response = requests.request("GET", url, headers=H.headers)
        response_text = response.text.replace("'",'"')
        my_response = json.loads(response_text)
        # //

        for x in range(1, ws.max_row+1):
            id = ws.cell(row = x, column = 1).value
            concentration = ws.cell(row = x, column = 5).value
            if id == my_response[x-1]['label']:
                payload = {'comments': 'payload_testing' + str(x),'origin': concentration,'volume': concentration}
                put_response = requests.request("PUT", H.put_url+my_response[x-1]['count'], headers=H.headers, data = payload)
                dict_list.append(dict(ID=id, conc=concentration,num=x, ct=my_response[x-1]['count'])) #count was excluded in dict_list

        return render_template("result.html", dict_list=dict_list)
    else:
        return render_template("update.html")
        
if __name__ == "__main__":
    app.run(debug=True)