from flask import Flask, request, jsonify
import pandas as pd
import io
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def calculate_revenue(initial_revenue, growth_rate, num_periods):
    revenue = [initial_revenue]
    for _ in range(num_periods):
        revenue.append(revenue[-1] * (1 + growth_rate))
    return revenue

#Grabs the xlsx file by default, processes the data for the front end
@app.route('/default-data', methods=['GET'])
def get_default_data():
    try:
        default_file_path = os.path.join(os.path.dirname(__file__), 'MVP Data.xlsx')
        df = pd.read_excel(default_file_path)

        # Process the data as you do in the upload_excel function
        labels = ['Historical']
        future_cols = [col for col in df.columns if 'Future' in str(col) or 'Unnamed' in str(col)][:4]

        for i, col in enumerate(future_cols):
            labels.append(f'Future {i+1}')

        initial_revenue = df.iloc[1, 2]

        scenarios = ["Base", "Upside", "Downside"]
        growth_rates = [float(df.iloc[1, 12]), float(df.iloc[2, 12]), float(df.iloc[3, 12])]

        revenue_data = {}
        for i, scenario in enumerate(scenarios):
            growth_rate = growth_rates[i]
            revenue_data[scenario] = calculate_revenue(initial_revenue, growth_rate, len(labels)-1)

        data = {
            'labels': labels,
            'scenarios': scenarios,
            'revenue_data': revenue_data,
            'growth_rates': {scenario: rate for scenario, rate in zip(scenarios, growth_rates)}
        }

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

#back end processing for user file upload
@app.route('/upload', methods=['POST'])
def upload_excel():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and file.filename.endswith('.xlsx'):
        try:
            excel_data = io.BytesIO(file.read())
            df = pd.read_excel(excel_data)

            labels = ['Historical']
            future_cols = [col for col in df.columns if 'Future' in str(col) or 'Unnamed' in str(col)][:4]
            for i, col in enumerate(future_cols):
                labels.append(f'Future {i+1}')

            initial_revenue = df.iloc[1, 2]

            scenarios = df.iloc[1:5, 11].tolist()
            growth_rates = df.iloc[1:5, 12].astype(float).tolist()

            revenue_data = {}
            for i, scenario in enumerate(scenarios):

                growth_rate = growth_rates[i]
                revenue_data[scenario] = calculate_revenue(initial_revenue, growth_rate, len(labels)-1)
            
            data = {
                'labels': labels,
                'scenarios': scenarios,
                'revenue_data': revenue_data
            }

            return jsonify(data)

        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        return jsonify({'error': 'Invalid file type. Only .xlsx is allowed.'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


