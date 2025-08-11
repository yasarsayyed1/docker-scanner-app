import docker
import json
import subprocess
import os
from typing import Dict, List
import tempfile

def scan_image(image_name: str) -> List[Dict]:
    """
    Scans the Docker image in real-time using Trivy scanner.
    
    Args:
        image_name (str): The name/path of the Docker image to scan
    
    Returns:
        List[Dict]: List of vulnerabilities found
    """
    try:
        # Initialize Docker client
        client = docker.from_env()
        
        # Pull the image if not present locally
        print(f"Pulling image: {image_name}")
        client.images.pull(image_name)
        
        # Create temporary file for JSON output
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        temp_file.close()
        
        # Run Trivy scan
        print(f"Scanning image: {image_name}")
        cmd = [
            "trivy",
            "image",
            "-f", "json",
            "-o", temp_file.name,
            image_name
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Stream the output in real-time
        while True:
            output = process.stderr.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        # Read scan results
        with open(temp_file.name, 'r') as f:
            scan_data = json.load(f)
        
        # Clean up temp file
        os.unlink(temp_file.name)
        
        # Process and format results
        return process_results(scan_data)
        
    except docker.errors.ImageNotFound:
        raise Exception(f"Image not found: {image_name}")
    except docker.errors.APIError as e:
        raise Exception(f"Docker API error: {str(e)}")
    except Exception as e:
        raise Exception(f"Scanning error: {str(e)}")

def process_results(scan_data: Dict) -> List[Dict]:
    """
    Process and format the Trivy scan results.
    
    Args:
        scan_data (Dict): Raw scan results from Trivy
    
    Returns:
        List[Dict]: Formatted vulnerability information
    """
    vulnerabilities = []
    
    for result in scan_data.get('Results', []):
        for vuln in result.get('Vulnerabilities', []):
            vulnerabilities.append({
                'vulnerability': vuln.get('VulnerabilityID', ''),
                'severity': vuln.get('Severity', 'UNKNOWN'),
                'description': vuln.get('Description', ''),
                'fix_version': vuln.get('FixedVersion', 'Not available')
            })
    
    return sorted(vulnerabilities, 
                 key=lambda x: {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3, 'UNKNOWN': 4}[x['severity']])