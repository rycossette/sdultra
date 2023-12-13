from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('sdultra.html')

@app.route('/generate', methods=['POST'])
def generate():
    payload = request.json
    response = requests.post('http://127.0.0.1:7860/sdapi/v1/txt2img', json=payload)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5001)

