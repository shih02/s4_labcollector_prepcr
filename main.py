from flask import Flask, render_template, request
import requests
import re
import H

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/result", methods=["POST"])
def result():
    name = request.form.get("name")
    H.url + name
    print(H.url+name)
    response_text = requests.request("GET", H.url, headers=H.headers).text
    return render_template("result.html", name=response_text)

@app.route("/update")
def update():
    return render_template("update.html")
    
if __name__ == "__main__":
    app.run(debug=True)

