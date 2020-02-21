from flask import Flask, render_template, request
import requests
import re
import H
from openpyxl import load_workbook, workbook

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/result", methods=["POST"])
def result():
    
    samplelist = ""
    name = request.form.get("name") #this is for searching
    wb = load_workbook(filename = 'Book1.xlsx')
    ws = wb['Sheet1']

    for x in range(1, ws.max_row+1):
        id = ws.cell(row = x, column = 1).value
        samplelist = samplelist + id +","

    #generate response and set response variables 
    # // careful with this loop as it can break LC server!!
    url = H.url_v2 + samplelist
    response = requests.request("GET", url, headers=H.headers)
    response_code = response.status_code
    response_text = response.text
    dict_list = []
    # //

    #rebuild response text to set count:lab id:volume
    sample = samplelist.split(",")
    for i in range(x):
        result = response_text.find(sample[i])
        res_split = re.split(r'[,:]',response_text[result-53:result+195])
        #count = res_split[1]
        volume = res_split[21]
        #sample_dict = dict(ID=sample[i], conc=eval(volume))
        dict_list.append(dict(ID=sample[i], conc=eval(volume)))
    
    return render_template("result.html", dict_list=dict_list)
    
@app.route("/update")
def update():

    wb = load_workbook(filename = 'Book1.xlsx')
    ws = wb['Sheet1']
    dict_list = []

    for x in range(1, ws.max_row+1):
        id = ws.cell(row = x, column = 1).value
        concentration = ws.cell(row = x, column = 2).value
        url = H.url + id
        response = requests.request("GET", url, headers=H.headers)
        res_split = re.split(r'[,:""]',response.text)
        print(res_split)
        count = res_split[4] #internal LC ID
        payload = {'comments': 'VS testing' + str(x),'origin': concentration,'volume': concentration}
        put_response = requests.request("PUT", H.put_url+count, headers=H.headers, data = payload)
        dict_list.append(dict(ID=id, conc=concentration, ct = count))
    
    return render_template("update.html", dict_list=dict_list)
    
if __name__ == "__main__":
    app.run(debug=True, port="3134")