from flask import Flask, request, render_template, redirect, url_for, session
import numpy as np
import pickle

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# Load the vectorizer and model
with open('vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)  # Assuming the vectorizer is saved in 'vectorizer.pkl'

with open('model.pkl', 'rb') as file:
    model = pickle.load(file)  # Assuming the trained spam detection model is saved in 'spam_model.pkl'

# Dummy credentials for login (username: admin, password: password)
USERNAME = 'admin'
PASSWORD = 'password'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('predict'))
        else:
            return render_template('login.html', error='Invalid Credentials. Please try again.')
    
    return render_template('login.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Get input values from the form (assume 'message' is the field for input text)
        message = request.form['message']
        
        # Preprocess the input text (vectorization)
        input_data = vectorizer.transform([message])  # Transform the input message using the vectorizer
        print(input_data)  # Optional: Print the transformed input data

        # Make prediction
        prediction = model.predict(input_data)
        print(prediction)  # Optional: Print the prediction (0 or 1)
        
        # 0: Not Spam, 1: Spam
        result = 'Spam' if prediction[0] == 1 else 'Not Spam'

        return render_template('result.html', prediction=result)
    
    return render_template('index.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
