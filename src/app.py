from flask import Flask, render_template, request, jsonify
from scanner import scan_image  # Note: scanner.py should be in the same directory
import re

app = Flask(__name__)

def validate_image_name(image_name):
    """Validate docker image name/path format"""
    pattern = r'^([a-zA-Z0-9]+(?:[._-][a-zA-Z0-9]+)*(?::[a-zA-Z0-9]+(?:[._-][a-zA-Z0-9]+)*)?/)?[a-zA-Z0-9]+(?:[._-][a-zA-Z0-9]+)*(?::[a-zA-Z0-9]+(?:[._-][a-zA-Z0-9]+)*)?$'
    return bool(re.match(pattern, image_name))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    image_name = request.form['image_name']
    
    if not image_name:
        return jsonify({'error': 'Image name is required'}), 400
    
    if not validate_image_name(image_name):
        return jsonify({'error': 'Invalid image name format'}), 400
    
    try:
        results = scan_image(image_name)
        return render_template('results.html', results=results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)