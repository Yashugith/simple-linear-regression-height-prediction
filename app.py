import json
import pickle
from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

# Load the model
regmodel = pickle.load(open("regmodel.pkl", "rb"))
scalar = pickle.load(open("scaler.pkl", "rb"))


# ------------ WELCOME PAGE ------------
@app.route("/")
def welcome():
    return render_template("welcome.html")


# ------------ HOME (PREDICTION FORM) ------------
@app.route("/home")
def home():
    return render_template("home.html")


# ------------ API FOR POSTMAN ------------
@app.route("/predict_api", methods=["POST"])
def predict_api():
    data = request.json["data"]
    new_data = scalar.transform(np.array(list(data.values())).reshape(1, -1))
    output = regmodel.predict(new_data)
    return jsonify(output[0])


# ------------ FORM SUBMISSION PREDICTION ------------
@app.route("/predict", methods=["POST"])
def predict():
    data = [float(x) for x in request.form.values()]
    final_input = scalar.transform(np.array(data).reshape(1, -1))

    # Predict height in cm
    height_cm = regmodel.predict(final_input)[0]

    # Convert to ft + inches
    height_in = height_cm / 2.54
    feet = int(height_in // 12)
    inches = round(height_in % 12, 1)

    result_text = f"Predicted Height: {height_cm:.2f} cm<br>{feet} ft {inches} inches"

    return render_template("home.html", prediction_text=result_text)


if __name__ == "__main__":
    app.run(debug=True)
