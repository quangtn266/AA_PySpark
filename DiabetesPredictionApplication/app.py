from flask import Flask, render_template, request
import pickle
import numpy as np

# load machine learning model
filename ="./models/model.pkl"
clf = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        preg = int(request.form['pregnancies'])
        glucose = int(request.form['glucose'])
        bp = int(request.form['bloodpressure'])
        st = int(request.form['skinthickness'])
        insulin = int(request.form['insulin'])
        bmi = int(request.form['bmi'])
        dpf = int(request.form['dpf'])
        age = int(request.form['age'])

        data = np.array([[preg, glucose, bp, st, insulin, bmi, dpf, age]])
        pred = clf.predict(data)

        return render_template('result.html', prediction=pred)

if __name__ == '__main__':
    app.run(debug=True)