#!/bin/bash

# Print Trivy version for verification
echo "Checking Trivy installation..."
trivy --version

# Start the Flask application with gunicorn
echo "Starting web application..."
gunicorn --bind 0.0.0.0:$PORT app:app