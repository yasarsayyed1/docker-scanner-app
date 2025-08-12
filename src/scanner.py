import docker
import json
import subprocess
import os
from typing import Dict, List
import tempfile
import platform
import socket

def get_docker_client():
    """Get Docker client with proper configuration for Windows"""
    error_messages = []
    
    # Check if Docker Desktop is running
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 2375))
        sock.close()
        if result != 0:
            error_messages.append("Docker Desktop is not running")
    except:
        error_messages.append("Could not check Docker Desktop status")

    # Try Windows named pipe
    try:
        client = docker.from_env(environment={
            'DOCKER_HOST': 'npipe:////./pipe/docker_engine'
        })
        client.ping()
        return client
    except Exception as e:
        error_messages.append(f"Named pipe connection failed: {str(e)}")

    # Try TCP connection
    try:
        client = docker.from_env(environment={
            'DOCKER_HOST': 'tcp://localhost:2375'
        })
        client.ping()
        return client
    except Exception as e:
        error_messages.append(f"TCP connection failed: {str(e)}")

    # If all connection attempts fail, raise detailed error
    raise Exception("\n".join([
        "Cannot connect to Docker. Please ensure:",
        "1. Docker Desktop is installed and running",
        "2. Docker is switched to Linux containers",
        "3. You have permissions to access Docker",
        f"Errors encountered: {'; '.join(error_messages)}"
    ]))

def scan_image(image_name: str) -> List[Dict]:
    """Scans the Docker image using Trivy"""
    try:
        # Get Docker client
        client = get_docker_client()
        
        print(f"Attempting to pull image: {image_name}")
        try:
            client.images.pull(image_name)
        except docker.errors.APIError as e:
            print(f"Pull error: {str(e)}")
            # Continue anyway as image might exist locally
        
        # Run Trivy scan
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()
        
        cmd = [
            "trivy",
            "image",
            "--format", "json",
            "--output", temp_file.name,
            image_name
        ]
        
        try:
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            with open(temp_file.name, 'r') as f:
                results = json.load(f)
            
            return process_results(results)
            
        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
                
    except Exception as e:
        raise Exception(f"Scanning error: {str(e)}")

def process_results(results: Dict) -> List[Dict]:
    vulnerabilities = []
    for result in results.get('Results', []):
        for vuln in result.get('Vulnerabilities', []):
            vulnerabilities.append({
                'vulnerability': vuln.get('VulnerabilityID', ''),
                'severity': vuln.get('Severity', 'UNKNOWN'),
                'description': vuln.get('Description', ''),
                'fix_version': vuln.get('FixedVersion', 'Not available')
            })
    return vulnerabilities