"""
Export trained model weights to JSON format for GitHub Pages deployment.
This allows the Python model to be used in the JavaScript/GitHub Pages version.
"""

import json
import numpy as np
from autoencoder import SensorAutoencoder

def export_model_to_json(filepath='model_weights.json'):
    """Train and export model weights to JSON"""
    
    print("🤖 Initializing Sensor Autoencoder...")
    model = SensorAutoencoder()
    
    print("📊 Generating training data...")
    # Generate normal operational data
    training_data = []
    for _ in range(1000):
        sample = []
        for _ in range(8):
            # Normal sensor readings (0-100)
            sample.append(np.random.normal(50, 15))
        training_data.append(np.clip(sample, 0, 100))
    
    print("🔄 Training model...")
    training_data = np.array(training_data)
    result = model.train(training_data, epochs=50)
    
    print(f"✅ Training complete. Final loss: {model.training_loss[-1]:.6f}")
    
    # Convert weights to JSON-serializable format
    weights_dict = {
        'W1': model.W1.tolist(),
        'b1': model.b1.tolist(),
        'W2': model.W2.tolist(),
        'b2': model.b2.tolist(),
        'W3': model.W3.tolist(),
        'b3': model.b3.tolist(),
        'W4': model.W4.tolist(),
        'b4': model.b4.tolist(),
        'threshold': float(model.threshold),
        'training_loss': model.training_loss,
        'n_features': int(model.n_features),
        'is_trained': True
    }
    
    # Save to JSON
    with open(filepath, 'w') as f:
        json.dump(weights_dict, f, indent=2)
    
    print(f"💾 Model weights exported to {filepath}")
    print(f"📦 File size: {len(json.dumps(weights_dict)) / 1024:.2f} KB")
    
    return weights_dict

if __name__ == '__main__':
    export_model_to_json('model_weights.json')
    print("\n✨ Model is ready for GitHub Pages deployment!")
    print("📋 Use the index-gh-pages.html with the model_weights.json file")
