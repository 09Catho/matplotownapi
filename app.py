from flask import Flask, request, send_file, jsonify
import matplotlib
matplotlib.use('Agg')  # For headless servers
import matplotlib.pyplot as plt
import numpy as np
import io
import traceback
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'Matplotlib Graph Render API is live!', 200

@app.route('/render-matplotlib', methods=['POST'])
def render_matplotlib():
    data = request.json or {}
    code = data.get("code", "")

    if not code:
        return jsonify({"error": "Missing code"}), 400

    # Setup a fresh plot context
    plt.close('all')
    buf = io.BytesIO()

    # Allow only safe builtins (very basic sandboxing)
    safe_globals = {"plt": plt, "np": np, "__builtins__": {}}
    try:
        exec(code, safe_globals)
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=200)
        plt.close()
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        plt.close()
        return jsonify({"error": traceback.format_exc()}), 500

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 5150))
    app.run(host='0.0.0.0', port=PORT)
