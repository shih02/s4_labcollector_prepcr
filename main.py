from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/result", methods=["POST"])
def result():
    #name = request.form.get("name")
    return render_template("result.html", name=text)

@app.route("/update")
def update():
    return render_template("update.html")
    
if __name__ == "__main__":
    app.run(debug=True)
