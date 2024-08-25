from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        # Load data and calculate BSI
        data = pd.read_csv(filepath)
        height = data['Height'].mean()  # Replace with actual data extraction logic
        waist_circumference = data['WaistCircumference'].mean()  # Replace with actual data extraction logic
        weight = data['Weight'].mean()  # Replace with actual data extraction logic
        
        bsi_value = calculate_bsi(height, waist_circumference, weight)
        
        return redirect(url_for('analyze', bsi_value=bsi_value))

@app.route('/analyze')
def analyze():
    bsi_value = request.args.get('bsi_value', None)
    return render_template('analysis.html', bsi_value=bsi_value)

def calculate_bsi(height, waist_circumference, weight):
    bsi_value = waist_circumference / (weight**(2/3) * height**(1/2))
    return bsi_value

if __name__ == '__main__':
    app.run(debug=True)
