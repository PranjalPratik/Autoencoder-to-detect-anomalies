import numpy as np
from sklearn.preprocessing import MinMaxScaler
import json

# Pure numpy autoencoder - no tensorflow dependency
class SensorAutoencoder:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.is_trained = False
        self.threshold = 0.05
        self.training_loss = []
        self.n_features = 8
        self.metrics = {
            'true_positives': 0,
            'false_positives': 0,
            'true_negatives': 0,
            'false_negatives': 0,
            'total_detections': 0,
            'anomalies_found': 0
        }

        # Encoder weights: 8 -> 4 -> 2
        self.W1 = np.random.randn(8, 4) * 0.1
        self.b1 = np.zeros(4)
        self.W2 = np.random.randn(4, 2) * 0.1
        self.b2 = np.zeros(2)
        # Decoder weights: 2 -> 4 -> 8
        self.W3 = np.random.randn(2, 4) * 0.1
        self.b3 = np.zeros(4)
        self.W4 = np.random.randn(4, 8) * 0.1
        self.b4 = np.zeros(8)

    def relu(self, x):
        return np.maximum(0, x)

    def relu_grad(self, x):
        return (x > 0).astype(float)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    def sigmoid_grad(self, x):
        s = self.sigmoid(x)
        return s * (1 - s)

    def forward(self, X):
        # Encoder
        self.z1 = X @ self.W1 + self.b1
        self.a1 = self.relu(self.z1)
        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = self.relu(self.z2)  # latent
        # Decoder
        self.z3 = self.a2 @ self.W3 + self.b3
        self.a3 = self.relu(self.z3)
        self.z4 = self.a3 @ self.W4 + self.b4
        self.a4 = self.sigmoid(self.z4)  # output
        return self.a4

    def backward(self, X, lr=0.01):
        m = X.shape[0]
        loss = np.mean((self.a4 - X) ** 2)

        # Output layer gradients
        dL_da4 = 2 * (self.a4 - X) / m
        dL_dz4 = dL_da4 * self.sigmoid_grad(self.z4)
        dL_dW4 = self.a3.T @ dL_dz4
        dL_db4 = dL_dz4.sum(axis=0)

        # Decoder hidden layer
        dL_da3 = dL_dz4 @ self.W4.T
        dL_dz3 = dL_da3 * self.relu_grad(self.z3)
        dL_dW3 = self.a2.T @ dL_dz3
        dL_db3 = dL_dz3.sum(axis=0)

        # Latent layer
        dL_da2 = dL_dz3 @ self.W3.T
        dL_dz2 = dL_da2 * self.relu_grad(self.z2)
        dL_dW2 = self.a1.T @ dL_dz2
        dL_db2 = dL_dz2.sum(axis=0)

        # Encoder hidden layer
        dL_da1 = dL_dz2 @ self.W2.T
        dL_dz1 = dL_da1 * self.relu_grad(self.z1)
        dL_dW1 = X.T @ dL_dz1
        dL_db1 = dL_dz1.sum(axis=0)

        # Update weights
        self.W4 -= lr * dL_dW4
        self.b4 -= lr * dL_db4
        self.W3 -= lr * dL_dW3
        self.b3 -= lr * dL_db3
        self.W2 -= lr * dL_dW2
        self.b2 -= lr * dL_db2
        self.W1 -= lr * dL_dW1
        self.b1 -= lr * dL_db1

        return loss

    def generate_normal_data(self, n_samples=1000):
        """Generate synthetic normal industrial sensor readings"""
        np.random.seed(42)
        t = np.linspace(0, 4 * np.pi, n_samples)

        data = np.column_stack([
            60 + 5 * np.sin(t) + np.random.normal(0, 1, n_samples),        # Temperature (°C)
            1.0 + 0.1 * np.cos(t) + np.random.normal(0, 0.02, n_samples),  # Pressure (bar)
            1500 + 50 * np.sin(2*t) + np.random.normal(0, 10, n_samples),  # RPM
            20 + 2 * np.sin(t + 1) + np.random.normal(0, 0.5, n_samples),  # Vibration (mm/s)
            220 + 5 * np.cos(t) + np.random.normal(0, 1, n_samples),       # Voltage (V)
            10 + 1 * np.sin(t + 2) + np.random.normal(0, 0.2, n_samples),  # Current (A)
            40 + 3 * np.cos(2*t) + np.random.normal(0, 0.5, n_samples),    # Flow rate (L/min)
            50 + 5 * np.sin(t + 3) + np.random.normal(0, 1, n_samples),    # Humidity (%)
        ])
        return data

    def generate_and_train(self, n_samples=1000, epochs=50):
        normal_data = self.generate_normal_data(n_samples)
        scaled_data = self.scaler.fit_transform(normal_data)

        self.training_loss = []
        lr = 0.01
        batch_size = 32
        loss_history = []

        for epoch in range(epochs):
            idx = np.random.permutation(len(scaled_data))
            epoch_loss = 0
            n_batches = 0

            for start in range(0, len(scaled_data), batch_size):
                batch = scaled_data[idx[start:start+batch_size]]
                self.forward(batch)
                loss = self.backward(batch, lr=lr)
                epoch_loss += loss
                n_batches += 1

            avg_loss = epoch_loss / n_batches
            loss_history.append(round(avg_loss, 6))
            if (epoch + 1) % 5 == 0:
                self.training_loss.append({'epoch': epoch + 1, 'loss': round(avg_loss, 6)})

        # Compute reconstruction errors on training data to set threshold
        recon = self.forward(scaled_data)
        errors = np.mean((scaled_data - recon) ** 2, axis=1)
        self.threshold = float(np.percentile(errors, 95))
        self.is_trained = True

        # Generate full loss curve (sampled to ~20 points for chart)
        step = max(1, epochs // 20)
        loss_curve = [{'epoch': i+1, 'loss': loss_history[i]} for i in range(0, epochs, step)]

        return {
            'success': True,
            'epochs': epochs,
            'final_loss': round(loss_history[-1], 6),
            'threshold': round(self.threshold, 6),
            'loss_curve': loss_curve,
            'n_samples': n_samples,
            'architecture': '8→4→2→4→8'
        }

    def detect_anomaly(self, sensor_values):
        if not self.is_trained:
            return {'error': 'Model not trained yet'}

        arr = np.array(sensor_values, dtype=float).reshape(1, -1)
        if arr.shape[1] != self.n_features:
            return {'error': f'Expected {self.n_features} features, got {arr.shape[1]}'}

        scaled = self.scaler.transform(arr)
        recon = self.forward(scaled)
        error = float(np.mean((scaled - recon) ** 2))
        is_anomaly = error > self.threshold
        score = min(100, int((error / (self.threshold * 2)) * 100))

        self.metrics['total_detections'] += 1
        if is_anomaly:
            self.metrics['anomalies_found'] += 1

        feature_errors = ((scaled - recon) ** 2)[0].tolist()
        sensor_names = ['Temperature', 'Pressure', 'RPM', 'Vibration', 'Voltage', 'Current', 'Flow Rate', 'Humidity']

        return {
            'is_anomaly': bool(is_anomaly),
            'reconstruction_error': round(error, 6),
            'threshold': round(self.threshold, 6),
            'anomaly_score': score,
            'confidence': round(min(99.9, abs(error - self.threshold) / self.threshold * 100), 1),
            'feature_contributions': [
                {'name': n, 'error': round(e, 4)}
                for n, e in zip(sensor_names, feature_errors)
            ],
            'reconstructed': self.scaler.inverse_transform(recon)[0].tolist()
        }

    def simulate_scenario(self, scenario, n_points=50):
        if not self.is_trained:
            return {'error': 'Model not trained yet'}

        t = np.linspace(0, 4 * np.pi, n_points)
        results = []

        for i in range(n_points):
            if scenario == 'normal':
                vals = [
                    60 + 5 * np.sin(t[i]) + np.random.normal(0, 0.5),
                    1.0 + 0.1 * np.cos(t[i]) + np.random.normal(0, 0.01),
                    1500 + 50 * np.sin(2*t[i]) + np.random.normal(0, 5),
                    20 + 2 * np.sin(t[i]+1) + np.random.normal(0, 0.2),
                    220 + 5 * np.cos(t[i]) + np.random.normal(0, 0.5),
                    10 + 1 * np.sin(t[i]+2) + np.random.normal(0, 0.1),
                    40 + 3 * np.cos(2*t[i]) + np.random.normal(0, 0.3),
                    50 + 5 * np.sin(t[i]+3) + np.random.normal(0, 0.5),
                ]
            elif scenario == 'overheat':
                spike = 30 * max(0, np.sin(t[i] - np.pi)) if i > n_points//2 else 0
                vals = [
                    60 + 5 * np.sin(t[i]) + spike + np.random.normal(0, 1),
                    1.0 + 0.1 * np.cos(t[i]) + np.random.normal(0, 0.01),
                    1500 + 50 * np.sin(2*t[i]) + np.random.normal(0, 5),
                    20 + 2 * np.sin(t[i]+1) + np.random.normal(0, 0.2),
                    220 + 5 * np.cos(t[i]) + np.random.normal(0, 0.5),
                    10 + 1 * np.sin(t[i]+2) + np.random.normal(0, 0.1),
                    40 + 3 * np.cos(2*t[i]) + np.random.normal(0, 0.3),
                    50 + 5 * np.sin(t[i]+3) + np.random.normal(0, 0.5),
                ]
            elif scenario == 'vibration':
                vib_spike = 40 * abs(np.sin(5*t[i])) if i > n_points//3 else 0
                vals = [
                    60 + 5 * np.sin(t[i]) + np.random.normal(0, 0.5),
                    1.0 + 0.1 * np.cos(t[i]) + np.random.normal(0, 0.01),
                    1500 + 50 * np.sin(2*t[i]) + np.random.normal(0, 5),
                    20 + vib_spike + np.random.normal(0, 1),
                    220 + 5 * np.cos(t[i]) + np.random.normal(0, 0.5),
                    10 + 1 * np.sin(t[i]+2) + np.random.normal(0, 0.1),
                    40 + 3 * np.cos(2*t[i]) + np.random.normal(0, 0.3),
                    50 + 5 * np.sin(t[i]+3) + np.random.normal(0, 0.5),
                ]
            elif scenario == 'power_surge':
                surge = 60 * (np.random.random() > 0.85) if i > n_points//4 else 0
                vals = [
                    60 + 5 * np.sin(t[i]) + np.random.normal(0, 0.5),
                    1.0 + 0.1 * np.cos(t[i]) + np.random.normal(0, 0.01),
                    1500 + 50 * np.sin(2*t[i]) + np.random.normal(0, 5),
                    20 + 2 * np.sin(t[i]+1) + np.random.normal(0, 0.2),
                    220 + surge + 5 * np.cos(t[i]) + np.random.normal(0, 0.5),
                    10 + 5 * (surge > 0) + 1 * np.sin(t[i]+2) + np.random.normal(0, 0.1),
                    40 + 3 * np.cos(2*t[i]) + np.random.normal(0, 0.3),
                    50 + 5 * np.sin(t[i]+3) + np.random.normal(0, 0.5),
                ]
            else:
                vals = [60, 1.0, 1500, 20, 220, 10, 40, 50]

            result = self.detect_anomaly(vals)
            result['timestamp'] = i
            result['raw_values'] = [round(v, 2) for v in vals]
            results.append(result)

        anomaly_count = sum(1 for r in results if r['is_anomaly'])
        return {
            'scenario': scenario,
            'n_points': n_points,
            'anomaly_rate': round(anomaly_count / n_points * 100, 1),
            'results': results
        }

    def get_metrics(self):
        total = self.metrics['total_detections']
        anomalies = self.metrics['anomalies_found']
        return {
            'is_trained': self.is_trained,
            'threshold': round(self.threshold, 6) if self.is_trained else None,
            'total_detections': total,
            'anomalies_found': anomalies,
            'normal_found': total - anomalies,
            'anomaly_rate': round(anomalies / total * 100, 1) if total > 0 else 0,
            'architecture': '8→4→2→4→8',
            'n_features': self.n_features,
            'sensor_names': ['Temperature', 'Pressure', 'RPM', 'Vibration', 'Voltage', 'Current', 'Flow Rate', 'Humidity']
        }
