import sys
import os
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app import create_app

def start_integrated_server():
    # 1. Initialize the backend app
    backend_app = create_app()
    
    # 2. Setup the main app that serves both
    app = Flask(__name__, static_folder='frontend')
    CORS(app) # Enable CORS for development
    
    # Register all backend blueprints to the main app
    for blueprint in backend_app.blueprints.values():
        # Important: backend blueprints already have /api prefix in their url_prefix
        app.register_blueprint(blueprint)

    # 3. Serve Frontend Static Files
    @app.route('/')
    def serve_index():
        return send_from_directory('frontend', 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        if os.path.exists(os.path.join('frontend', path)):
            return send_from_directory('frontend', path)
        return send_from_directory('frontend', 'index.html') # Fallback for SPA-like behavior

    # 4. Health Check
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "service": "unified_server"})

    # Log all requests for debugging
    @app.before_request
    def log_request_info():
        if not request.path.startswith('/js/') and not request.path.startswith('/css/'):
            print(f"📥 Request: {request.method} {request.path}")

    print("\n" + "="*50)
    print("🚀 India Guide Unified Server is LIVE!")
    print("👉 URL: http://localhost:5000")
    print("👉 Serving: Frontend + API + Map Service")
    print("="*50 + "\n")
    
    # Run the unified server
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

if __name__ == "__main__":
    start_integrated_server()