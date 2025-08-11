FROM python:3.9-slim

# Install system dependencies and Trivy
RUN apt-get update && apt-get install -y wget apt-transport-https gnupg lsb-release
RUN wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | apt-key add -
RUN echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | tee -a /etc/apt/sources.list.d/trivy.list
RUN apt-get update && apt-get install -y trivy

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD gunicorn --bind 0.0.0.0:$PORT app:app