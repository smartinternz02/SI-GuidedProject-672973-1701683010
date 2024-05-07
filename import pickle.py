import pickle
from flask import Flask, request, render_template

app = Flask(__name__)

model = pickle.load(open("logistic_regression_model.pkl", "rb"))

@app.route('/home')
def home():
    return render_template('index.html')

@app.route("/details", methods=["GET", "POST"])
def pred():
    return render_template('details.html')

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        low = float(request.form.get("low"))
        high = float(request.form.get("high"))
        volume = float(request.form.get("volume"))
        open = float(request.form.get("open"))
        company = str(request.form.get("company"))
        year = int(request.form.get("year"))
        month = int(request.form.get("month"))
        day = int(request.form.get("day"))
        print(year)
        xx = model.predict([[open, high, low, volume, year, month, day, company]])
        out = xx[0]
        print("Forecasted closing price on {}/{}/{} is $ {}".format(day, month, year, out))
        return render_template("result.html",
                               p="Forecasted closing price on {}/{}/{} is $ {}".format(day, month, year, out))

if __name__ == '__main__':
    app.run(debug=False)
