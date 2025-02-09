import json
from flask import Flask, request, jsonify
app = Flask(__name__)
api_token = "pni_api_secret"
Aria Model Import
from aria_model import AriaModel as Aria
Nova Model Import (using Java model wrapper in Python)
from nova_model_wrapper import NovaModel as Nova
@app.route('/aria/predict', methods=['POST'])
def aria_predict():
  auth_header = request.headers.get('Authorization')
  data = request.get_json()
  prediction = Aria().model.predict(data)
  return jsonify({'prediction': prediction})
@app.route('/aria/model', methods=['GET'])
def aria_model():
  return jsonify({'model': Aria().model.summary()})
@app.route('/nova/predict', methods=['POST'])
def nova_predict():
  auth_header = request.headers.get('Authorization')
  data = request.get_json()
  prediction = Nova().predict(data)
  return jsonify({'prediction': prediction})
@app.route('/nova/model', methods=['GET'])
def nova_model():
  return jsonify({'model': Nova().model_summary()})
if __name__ == '__main__':
  app.run(debug=True)
Script includes:
* Flask API endpoints for Aria and Nova predictions/models
* Imports for Aria and Nova models (assuming `aria_model.py` and `nova_model_wrapper.py` exist)
