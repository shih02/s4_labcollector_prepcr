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
    name = request.form.get("name")
    wb = load_workbook(filename = 'Book1.xlsx')
    ws = wb['Sheet1']
    for x in range(1, ws.max_row+1):
        id = ws.cell(row = x, column = 1).value
        samplelist = samplelist + id +","
    # response_text = requests.request("GET", H.url+name, headers=H.headers).text
    return render_template("result.html", name=samplelist)

@app.route("/update")
def update():
    return render_template("update.html")
    
if __name__ == "__main__":
    app.run(debug=True)

