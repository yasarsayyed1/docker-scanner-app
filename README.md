# docker-scanner-app

This project is a Docker image vulnerability scanner built with Flask. It allows users to input a Docker image name and receive a report on any known vulnerabilities associated with that image.

## Project Structure

```
docker-scanner-app
├── src
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   └── js
│   │       └── main.js
│   ├── templates
│   │   ├── base.html
│   │   ├── index.html
│   │   └── results.html
│   ├── app.py
│   ├── scanner.py
│   └── config.py
├── tests
│   └── test_app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd docker-scanner-app
   ```

2. **Install dependencies:**
   Make sure you have Python and pip installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   Create a `.env` file in the root directory and add your configuration settings.

4. **Run the application:**
   You can run the application using Docker:
   ```bash
   docker-compose up
   ```

5. **Access the application:**
   Open your web browser and go to `http://localhost:5000` to access the scanner interface.

## Usage

- Enter the Docker image name (e.g., `nginx:latest`) in the provided form.
- Submit the form to initiate the vulnerability scan.
- View the results on the results page, which will display any CVEs found.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.