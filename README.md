# Matplotlib Graph Render API

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A robust, containerized Flask API that allows you to execute Python code remotely to generate Matplotlib graphs. This service is designed for headless environments and includes authentication and basic logging.

## Features

-   **Headless Rendering:** Uses Matplotlib's Agg backend to render graphs without a display.
-   **Secure-ish Execution:** Executes user-provided Python code in a restricted scope (see Security Note).
-   **Authentication:** Protects endpoints with API Key authentication.
-   **Logging:** Structured logging for monitoring and debugging.
-   **Dockerized:** Ready for deployment using Docker.
-   **Tested:** Comprehensive test suite using `pytest`.

## Project Structure

```
.
├── src/
│   ├── app.py          # Main Flask application
│   ├── config.py       # Configuration management
│   └── executor.py     # Code execution logic
├── tests/              # Unit tests
├── Dockerfile          # Container definition
├── Makefile            # Convenience commands
└── requirements.txt    # Python dependencies
```

## Getting Started

### Prerequisites

-   Python 3.10+
-   Pip

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/matplotlib-render-api.git
    cd matplotlib-render-api
    ```

2.  Install dependencies:
    ```bash
    make install
    # or
    pip install -r requirements.txt
    ```

3.  Set up environment variables:
    Create a `.env` file in the root directory:
    ```env
    PORT=5150
    API_KEY=your-secret-api-key
    DEBUG=True
    ```

### Running Locally

```bash
make run
# or
export API_KEY=my-secret-key
python -m src.app
```

The server will start at `http://0.0.0.0:5150`.

## API Documentation

### 1. Health Check

**GET** `/`

Returns a simple status message to verify the service is running.

-   **Response:** `200 OK`

### 2. Render Graph

**POST** `/render-matplotlib`

Executes the provided Python code and returns the generated graph as a PNG image.

-   **Headers:**
    -   `Content-Type: application/json`
    -   `X-API-Key: <your-api-key>`

-   **Body:**
    ```json
    {
      "code": "import numpy as np\nimport matplotlib.pyplot as plt\nx = np.linspace(0, 10, 100)\nplt.plot(x, np.sin(x))\n"
    }
    ```

-   **Response:**
    -   `200 OK`: Returns the PNG image (MIME type `image/png`).
    -   `400 Bad Request`: Missing code or invalid JSON.
    -   `401 Unauthorized`: Invalid or missing API Key.
    -   `500 Internal Server Error`: Error during code execution (returns error trace).

## Docker

Build and run the container:

```bash
docker build -t matplotlib-api .
docker run -p 5150:5150 -e API_KEY=secret matplotlib-api
```

## Testing

Run the test suite using `pytest`:

```bash
make test
# or
export PYTHONPATH=$PYTHONPATH:.
pytest
```

## Security Note

**⚠️ Warning:** This application uses Python's `exec()` function to execute arbitrary code sent by the client. While basic sandboxing is attempted, **it is not secure against malicious attacks**.
-   **Do not** expose this API publicly without strict firewalls and trusted clients.
-   The current implementation allows imports to facilitate library usage, which increases risk.
-   For a truly secure environment, consider running the execution logic inside an isolated ephemeral container (e.g., AWS Lambda, Firecracker microVMs).
