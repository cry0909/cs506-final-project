import pandas as pd
from flask import Flask, render_template, request, jsonify
import json
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

app = Flask(__name__)

# Preprocess data globally
data = pd.read_csv('data/train.csv')
data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], errors='coerce')
data['DayOfWeek'] = data['DateTime'].dt.day_name()
data['Hour'] = data['DateTime'].dt.hour
data['Wait Time (mins)'] = pd.to_numeric(data['Wait Time (mins)'], errors='coerce')
data.dropna(subset=['Wait Time (mins)'], inplace=True)

# Prepare global average wait time data
avg_wait_times = data.groupby(['DayOfWeek', 'Hour'])['Wait Time (mins)'].mean().reset_index()
avg_wait_times['DayOfWeek'] = pd.Categorical(
    avg_wait_times['DayOfWeek'], 
    categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
    ordered=True
)
avg_wait_times.sort_values('DayOfWeek', inplace=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Prepare average wait time chart data
    avg_wait_time_data = {
        "labels": avg_wait_times['DayOfWeek'].unique().tolist(),
        "datasets": [
            {
                "label": "Average Wait Time (mins)",
                "data": avg_wait_times.groupby('DayOfWeek')['Wait Time (mins)'].mean().tolist(),
                "backgroundColor": "rgba(75, 192, 192, 0.2)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 1
            }
        ]
    }

    # Prepare predicted vs actual chart data
    predictions = [15, 20, 25, 30]  # Example predictions (replace with actual model predictions)
    actuals = [14, 21, 23, 28]  # Example actual values (replace with actual values)
    hours = [7, 8, 9, 10]  # Example hours (replace with actual time data)

    pred_vs_actual_data = {
        "labels": hours,  # X-axis: hours
        "datasets": [
            {
                "label": "Actual Wait Time (mins)",
                "data": actuals,
                "backgroundColor": "rgba(75, 192, 192, 0.2)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 1
            },
            {
                "label": "Predicted Wait Time (mins)",
                "data": predictions,
                "backgroundColor": "rgba(255, 99, 132, 0.2)",
                "borderColor": "rgba(255, 99, 132, 1)",
                "borderWidth": 1
            }
        ]
    }

    return render_template(
        'index.html',
        avg_wait_time_data=json.dumps(avg_wait_time_data),
        pred_vs_actual_data=json.dumps(pred_vs_actual_data)
    )


@app.route('/results')
def results():
    chart_data, mse = prepare_chart_data()
    return render_template('results.html', mse=mse, chart_data=json.dumps(chart_data))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    day = data.get('day')
    time = data.get('time')

    if not day or time is None:
        return jsonify({'error': 'Missing day or time'}), 400

    try:
        time = int(time)
        if time < 0 or time > 23:
            return jsonify({'error': 'Time must be an integer between 0 and 23'}), 400
    except ValueError:
        return jsonify({'error': 'Time must be an integer'}), 400

    day_mapping = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
        "Friday": 4, "Saturday": 5, "Sunday": 6
    }

    if day not in day_mapping:
        return jsonify({'error': f"Invalid day: {day}. Valid days are {', '.join(day_mapping.keys())}"}), 400

    day_numeric = day_mapping[day]
    predicted_wait_time = 15 if day == "Monday" and time == 9 else 20  # Placeholder logic

    return jsonify({
        'day': day,
        'time': time,
        'predicted_wait_time': round(predicted_wait_time, 2)
    })


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
