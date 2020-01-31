from flask import Flask, render_template, request
import requests
import re

app = Flask(__name__)
#API header for labcollector
header  = {
'Accept': 'application/json;odata.metadata=full',
'X-LC-APP-Auth': 'b970d14af941f18aa1417c874e0f414db437fa6b277bf4c7ec196a189fc9f0c5',
'Host': '10.95.2.101',
'Accept-Encoding': 'gzip, deflate, br',
'Connection': 'keep-alive'
}
url = "http://10.95.2.101/lab/webservice/v1/samples?label="

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/result", methods=["POST"])
def result():
    name = request.form.get("name")
    url + name
    response_text = requests.request("GET", url, headers=header).text
    return render_template("result.html", name=response_text)

@app.route("/update")
def update():
    return render_template("update.html")
    
if __name__ == "__main__":
    app.run(debug=True)

