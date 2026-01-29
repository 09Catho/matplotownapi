from flask import Flask, request, send_file, jsonify
import traceback
import logging
from functools import wraps
from .config import Config
from .executor import execute_plot_code

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != app.config['API_KEY']:
            logger.warning("Unauthorized access attempt")
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    logger.info("Health check endpoint called")
    return 'Matplotlib Graph Render API is live!', 200

@app.route('/render-matplotlib', methods=['POST'])
@require_api_key
def render_matplotlib():
    logger.info("Render endpoint called")

    if not request.is_json:
        logger.warning("Request content-type is not JSON")
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json()
    code = data.get("code")

    if not code or not isinstance(code, str):
        logger.warning("Render request missing code or code is not a string")
        return jsonify({"error": "Missing or invalid 'code' field"}), 400

    try:
        logger.info("Executing plot code")
        buf = execute_plot_code(code)
        logger.info("Plot generated successfully")
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        logger.error(f"Error executing code: {e}")
        logger.error(traceback.format_exc())
        # In production, we might want to log the full trace but hide it from the user
        # keeping original behavior for now
        return jsonify({"error": traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['PORT'])
