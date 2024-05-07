from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Load the machine learning model
try:
    model = joblib.load('logistic_regression_model.pkl')
except FileNotFoundError:
    print("Error: Model file not found.")
    # You might want to handle this error more gracefully, depending on your use case.

# Map company names to numerical values
company_mapping = {'AMD': 0, 'ASUS': 1, 'INTEL': 2, 'MSI': 3, 'NVIDIA': 4}

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            low = float(request.form['Low'])
            high = float(request.form['High'])
            volume = float(request.form['Volume'])
            open_price = float(request.form['Open'])
            year = int(request.form['Year'])
            month = request.form['Month']
            day = int(request.form['Day'])
            company = request.form['Company']

            # Input validation can be added here

            month_mapping = {
                'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
            }
            month_numeric = month_mapping.get(month, 1)

            company_numeric = company_mapping.get(company, 0)

            input_data = [[low, high, volume, open_price, year, month_numeric, day, company_numeric]]
            prediction = model.predict(input_data)

            return render_template('prediction.html', result=prediction[0])
        except Exception as e:
            print(f"Error: {e}")
            return render_template('prediction.html', result=None, error="Invalid input. Please check your input values.")
    else:
        return render_template('prediction.html', result=None)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
