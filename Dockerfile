FROM python:3.9-slim

# Install system dependencies, Docker, and Trivy
RUN apt-get update && \
    apt-get install -y \
    wget \
    apt-transport-https \
    gnupg \
    lsb-release \
    ca-certificates \
    curl
    

# Install Trivy
RUN wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | apt-key add - && \
    echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | tee -a /etc/apt/sources.list.d/trivy.list && \
    apt-get update && \
    apt-get install -y trivy

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application with a startup script
COPY start.sh .
RUN chmod +x start.sh
CMD ["./start.sh"]