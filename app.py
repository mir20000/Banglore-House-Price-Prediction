from flask import Flask, jsonify, request, render_template
import pickle

app = Flask(__name__)
reg = pickle.load(open('reg_model.pkl', 'rb'))
lben = pickle.load(open('lben.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    location = request.form.get('location')
    total_sqft = float(request.form.get('total_sqft'))
    bath = float(request.form.get('bath'))
    bedrooms = float(request.form.get('bedrooms'))
    price_per_sqft = float(request.form.get('price_per_sqft'))

    int_bedrooms=int(bedrooms)
    int_location=int(lben.transform([location]))

    feature_list = [[int_location, total_sqft, bath, int_bedrooms, price_per_sqft]]

    prediction = reg.predict(feature_list)
    prediction = prediction*100000
    output = round(prediction[0], 2)

    return render_template('index.html', pretxt="The Price Of The House is Rs.{}".format(output))


if __name__ == "__main__":
    app.run()
