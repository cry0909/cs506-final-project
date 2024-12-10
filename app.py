import pandas as pd
from flask import Flask, render_template
import json
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

app = Flask(__name__)

# Load the data
data = pd.read_csv('data/train.csv')
def prepare_avg_wait_time_data():
    # Ensure 'DateTime' is a proper datetime object
    data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], errors='coerce')
    data['DayOfWeek'] = data['DateTime'].dt.day_name()
    data['Hour'] = data['DateTime'].dt.hour

    # Calculate the average wait time for each day of the week
    avg_wait_times = data.groupby(['DayOfWeek', 'Hour'])['Wait Time (mins)'].mean().reset_index()

    # Sort the days of the week
    avg_wait_times['DayOfWeek'] = pd.Categorical(
        avg_wait_times['DayOfWeek'], 
        categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
        ordered=True
    )
    avg_wait_times.sort_values('DayOfWeek', inplace=True)
    
    return avg_wait_times

def prepare_chart_data():
    # Preprocess the data
    data['Time'] = pd.to_datetime(data['Time'], format='%I:%M:%S %p')
    data['Hour'] = data['Time'].dt.hour
    data['Wait Time (mins)'] = pd.to_numeric(data['Wait Time (mins)'], errors='coerce')
    data.dropna(subset=['Wait Time (mins)'], inplace=True)

    # Prepare features and target
    X = data[['Hour']]
    y = data['Wait Time (mins)']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Decision Tree Regressor
    model = DecisionTreeRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Generate predictions
    predictions = model.predict(X)
    mse = mean_squared_error(y, predictions)

    # Prepare chart data
    chart_data = {
        "labels": data['Hour'].tolist(),  # X-axis (Hour of the day)
        "datasets": [
            {
                "label": 'Actual Wait Time (mins)',
                "data": y.tolist(),  # Actual wait times
                "backgroundColor": 'rgba(75, 192, 192, 0.2)',
                "borderColor": 'rgba(75, 192, 192, 1)',
                "borderWidth": 1
            },
            {
                "label": 'Predicted Wait Time (mins)',
                "data": predictions.tolist(),  # Predicted wait times
                "backgroundColor": 'rgba(255, 99, 132, 0.2)',
                "borderColor": 'rgba(255, 99, 132, 1)',
                "borderWidth": 1
            }
        ]
    }
    return chart_data, mse

@app.route('/')
def index():
    avg_wait_time_data = {
        "labels": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "datasets": [
            {
                "label": "Average Wait Time (mins)",
                "data": [10, 15, 12, 18, 20, 22, 15],
                "backgroundColor": "rgba(75, 192, 192, 0.2)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 1,
            }
        ],
        "xLabel": "Day of the Week",
        "yLabel": "Average Wait Time (mins)",
    }

    pred_vs_actual_data = {
        "labels": list(range(7, 22)),  # Hours of the day
        "datasets": [
            {
                "label": "Actual Wait Time (mins)",
                "data": [5, 6, 8, 12, 10, 15, 14, 18, 20, 22, 25, 28, 18, 15],
                "backgroundColor": "rgba(75, 192, 192, 0.2)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 1,
            },
            {
                "label": "Predicted Wait Time (mins)",
                "data": [4, 5, 7, 11, 9, 14, 13, 17, 19, 21, 24, 27, 17, 14],
                "backgroundColor": "rgba(255, 99, 132, 0.2)",
                "borderColor": "rgba(255, 99, 132, 1)",
                "borderWidth": 1,
            }
        ],
        "xLabel": "Hour of the Day",
        "yLabel": "Wait Time (mins)",
    }

    return render_template(
        'index.html',
        avg_wait_time_data=json.dumps(avg_wait_time_data),
        pred_vs_actual_data=json.dumps(pred_vs_actual_data),
    )

@app.route('/results')
def results():
    chart_data, mse = prepare_chart_data()  # Get MSE here
    return render_template('results.html', mse=mse, chart_data=json.dumps(chart_data))


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    print(app.url_map)  # Show all registered routes
    app.run(debug=True)
