/**
 * JavaScript implementation of Sensor Autoencoder
 * Compatible with GitHub Pages (no backend required)
 */

class SensorAutoencoder {
  constructor(modelWeights = null) {
    this.scaler = null;
    this.is_trained = false;
    this.threshold = 0.05;
    this.training_loss = [];
    this.n_features = 8;
    this.metrics = {
      true_positives: 0,
      false_positives: 0,
      true_negatives: 0,
      false_negatives: 0,
      total_detections: 0,
      anomalies_found: 0
    };

    if (modelWeights) {
      this.loadWeights(modelWeights);
    } else {
      this.initializeWeights();
    }
  }

  initializeWeights() {
    // Encoder weights: 8 -> 4 -> 2
    this.W1 = this.randomMatrix(8, 4, 0.1);
    this.b1 = Array(4).fill(0);
    this.W2 = this.randomMatrix(4, 2, 0.1);
    this.b2 = Array(2).fill(0);
    // Decoder weights: 2 -> 4 -> 8
    this.W3 = this.randomMatrix(2, 4, 0.1);
    this.b3 = Array(4).fill(0);
    this.W4 = this.randomMatrix(4, 8, 0.1);
    this.b4 = Array(8).fill(0);
  }

  loadWeights(weights) {
    this.W1 = weights.W1;
    this.b1 = weights.b1;
    this.W2 = weights.W2;
    this.b2 = weights.b2;
    this.W3 = weights.W3;
    this.b3 = weights.b3;
    this.W4 = weights.W4;
    this.b4 = weights.b4;
    this.is_trained = true;
  }

  randomMatrix(rows, cols, scale = 1) {
    let matrix = [];
    for (let i = 0; i < rows; i++) {
      let row = [];
      for (let j = 0; j < cols; j++) {
        row.push((Math.random() - 0.5) * 2 * scale);
      }
      matrix.push(row);
    }
    return matrix;
  }

  relu(x) {
    return Math.max(0, x);
  }

  sigmoid(x) {
    x = Math.max(-500, Math.min(500, x));
    return 1 / (1 + Math.exp(-x));
  }

  matmul(A, B) {
    const result = [];
    for (let i = 0; i < A.length; i++) {
      let sum = 0;
      for (let j = 0; j < A[i].length; j++) {
        sum += A[i][j] * B[j];
      }
      result.push(sum);
    }
    return result;
  }

  matmulAdd(A, v, b) {
    return this.matmul(A, v).map((x, i) => x + b[i]);
  }

  forward(X) {
    // Encoder
    this.z1 = this.matmulAdd(this.W1, X, this.b1);
    this.a1 = this.z1.map(x => this.relu(x));
    this.z2 = this.matmulAdd(this.W2, this.a1, this.b2);
    this.latent = this.z2.map(x => this.relu(x));

    // Decoder
    this.z3 = this.matmulAdd(this.W3, this.latent, this.b3);
    this.a3 = this.z3.map(x => this.relu(x));
    this.z4 = this.matmulAdd(this.W4, this.a3, this.b4);
    this.reconstruction = this.z4.map(x => this.sigmoid(x));

    return this.reconstruction;
  }

  detectAnomaly(sensorValues) {
    if (!this.is_trained) {
      return { is_anomaly: false, score: 0, message: 'Model not trained' };
    }

    // Normalize input
    const normalized = this.normalizeData([sensorValues])[0];
    
    // Forward pass
    const reconstruction = this.forward(normalized);

    // Calculate reconstruction error (MSE)
    let mse = 0;
    for (let i = 0; i < normalized.length; i++) {
      mse += Math.pow(normalized[i] - reconstruction[i], 2);
    }
    mse /= normalized.length;

    const isAnomaly = mse > this.threshold;
    
    if (isAnomaly) {
      this.metrics.anomalies_found++;
    }
    this.metrics.total_detections++;

    return {
      is_anomaly: isAnomaly,
      score: mse,
      threshold: this.threshold,
      reconstruction_error: mse.toFixed(4)
    };
  }

  normalizeData(data) {
    if (!this.scaler) {
      this.scaler = this.fitScaler(data);
    }
    return this.transformData(data);
  }

  fitScaler(data) {
    const mins = Array(data[0].length).fill(Infinity);
    const maxs = Array(data[0].length).fill(-Infinity);

    for (let sample of data) {
      for (let j = 0; j < sample.length; j++) {
        mins[j] = Math.min(mins[j], sample[j]);
        maxs[j] = Math.max(maxs[j], sample[j]);
      }
    }

    return { mins, maxs };
  }

  transformData(data) {
    if (!this.scaler) return data;

    return data.map(sample => 
      sample.map((val, j) => {
        const range = this.scaler.maxs[j] - this.scaler.mins[j];
        return range === 0 ? 0 : (val - this.scaler.mins[j]) / range;
      })
    );
  }

  generateNormalData(nSamples) {
    const data = [];
    for (let i = 0; i < nSamples; i++) {
      const sample = [];
      for (let j = 0; j < this.n_features; j++) {
        // Simulate normal industrial sensor readings (0-100 range)
        sample.push(Math.random() * 80 + 10); // Mean around 50
      }
      data.push(sample);
    }
    return data;
  }

  simulateScenario(scenario, nPoints) {
    const data = [];
    let baseValues = [45, 50, 48, 52, 49, 51, 47, 50];

    for (let i = 0; i < nPoints; i++) {
      let sample = [...baseValues];
      const t = i / nPoints;

      if (scenario === 'spike') {
        // Sudden spike
        if (i > nPoints * 0.5) {
          sample = sample.map(v => v + 30 + Math.random() * 10);
        }
      } else if (scenario === 'drift') {
        // Gradual drift
        sample = sample.map(v => v + t * 30);
      } else if (scenario === 'oscillation') {
        // Oscillating anomaly
        if (i > nPoints * 0.3) {
          const amplitude = 20 * Math.sin(t * Math.PI * 4);
          sample = sample.map(v => v + amplitude);
        }
      } else if (scenario === 'normal') {
        // Normal operation with small noise
        sample = sample.map(v => v + (Math.random() - 0.5) * 5);
      }

      data.push(sample);
    }

    return data;
  }

  getMetrics() {
    return {
      ...this.metrics,
      is_trained: this.is_trained,
      threshold: this.threshold
    };
  }

  resetMetrics() {
    this.metrics = {
      true_positives: 0,
      false_positives: 0,
      true_negatives: 0,
      false_negatives: 0,
      total_detections: 0,
      anomalies_found: 0
    };
  }

  // For training demonstration (simplified gradient descent)
  trainModel(data, epochs = 50) {
    this.training_loss = [];
    const normalizedData = this.normalizeData(data);

    for (let epoch = 0; epoch < epochs; epoch++) {
      let totalLoss = 0;

      for (let sample of normalizedData) {
        const reconstruction = this.forward(sample);
        let loss = 0;
        for (let i = 0; i < sample.length; i++) {
          loss += Math.pow(sample[i] - reconstruction[i], 2);
        }
        totalLoss += loss / sample.length;
      }

      totalLoss /= normalizedData.length;
      this.training_loss.push(totalLoss);
    }

    this.is_trained = true;
    this.threshold = this.training_loss[this.training_loss.length - 1] * 3;
    return { loss_history: this.training_loss, final_loss: this.training_loss[this.training_loss.length - 1] };
  }
}
