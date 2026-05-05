from flask import Flask, render_template, request, jsonify
import numpy as np
import json
import os
from autoencoder import SensorAutoencoder

app = Flask(__name__)
model = SensorAutoencoder()

print("FILES:", os.listdir())
print("TEMPLATES:", os.listdir("templates"))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/train', methods=['POST'])
def train():
    data = request.json
    n_samples = data.get('n_samples', 1000)
    epochs = data.get('epochs', 50)
    
    # Generate synthetic industrial sensor data (normal operation)
    result = model.generate_and_train(n_samples=n_samples, epochs=epochs)
    return jsonify(result)

@app.route('/api/detect', methods=['POST'])
def detect():
    data = request.json
    sensor_values = data.get('sensor_values', [])
    
    if not sensor_values:
        return jsonify({'error': 'No sensor values provided'}), 400
    
    result = model.detect_anomaly(sensor_values)
    return jsonify(result)

@app.route('/api/simulate', methods=['POST'])
def simulate():
    data = request.json
    scenario = data.get('scenario', 'normal')
    n_points = data.get('n_points', 50)
    
    result = model.simulate_scenario(scenario, n_points)
    return jsonify(result)

@app.route('/api/metrics', methods=['GET'])
def metrics():
    return jsonify(model.get_metrics())

@app.route('/api/batch_detect', methods=['POST'])
def batch_detect():
    data = request.json
    readings = data.get('readings', [])
    results = [model.detect_anomaly(r) for r in readings]
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
