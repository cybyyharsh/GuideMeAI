#!/usr/bin/env python3
"""
🚀 GuideMe - One-Click Startup Script
=====================================
This script starts the entire GuideMe application with all necessary checks.
Just run: python start.py
"""

import sys
import os
import subprocess
import time
import requests
from pathlib import Path

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(message):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(message):
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")

def check_python_version():
    """Check if Python version is compatible"""
    print_info("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python 3.8+ required. You have {version.major}.{version.minor}")
        return False
    print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    print_info("Checking dependencies...")
    
    required_packages = [
        'flask',
        'flask_cors',
        'requests',
        'dotenv',
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            elif package == 'flask_cors':
                __import__('flask_cors')
            else:
                __import__(package)
            print_success(f"{package} is installed")
        except ImportError:
            missing.append(package)
            print_error(f"{package} is missing")
    
    if missing:
        print_warning("\nInstalling missing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print_success("All dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print_error("Failed to install dependencies. Please run: pip install -r requirements.txt")
            return False
    
    print_success("All dependencies are installed")
    return True

def check_ollama():
    """Check if Ollama is running"""
    print_info("Checking Ollama service...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            print_success("Ollama is running")
            
            # Check if llama3 model is available
            models = response.json().get('models', [])
            model_names = [m.get('name', '') for m in models]
            
            if any('llama3' in name.lower() for name in model_names):
                print_success("llama3 model is available")
            else:
                print_warning("llama3 model not found. Available models:")
                for model in model_names:
                    print(f"  - {model}")
                print_info("You can pull llama3 with: ollama pull llama3")
            
            return True
    except requests.exceptions.RequestException:
        print_error("Ollama is not running!")
        print_info("Please start Ollama:")
        print_info("  - Windows: Start Ollama from Start Menu or run 'ollama serve'")
        print_info("  - Mac/Linux: Run 'ollama serve' in terminal")
        print_info("\nThen pull the model: ollama pull llama3")
        return False

def check_project_structure():
    """Verify project structure is intact"""
    print_info("Checking project structure...")
    
    required_paths = [
        'backend',
        'backend/app.py',
        'backend/routes',
        'backend/services',
        'index.html',
        'js',
        'css',
        'images'


    ]
    
    missing = []
    for path in required_paths:
        if not os.path.exists(path):
            missing.append(path)
            print_error(f"Missing: {path}")
        else:
            print_success(f"Found: {path}")
    
    if missing:
        print_error("Project structure is incomplete!")
        return False
    
    print_success("Project structure is valid")
    return True

def check_port_availability():
    """Check if port 5000 is available"""
    print_info("Checking if port 5000 is available...")
    
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 5000))
    sock.close()
    
    if result == 0:
        print_warning("Port 5000 is already in use!")
        print_info("Please close any application using port 5000 or the server might fail to start")
        return True  # Don't block, just warn
    
    print_success("Port 5000 is available")
    return True

def start_server():
    """Start the integrated server"""
    print_header("🚀 Starting GuideMeAI Server")
    
    # Add backend to Python path
    sys.path.append(os.path.join(os.getcwd(), 'backend'))
    
    # Import and start the server
    try:
        from flask import Flask, send_from_directory, jsonify, request
        from flask_cors import CORS
        from app import create_app
        
        # Initialize the backend app
        backend_app = create_app()
        
        # Setup the main app that serves both
        app = Flask(__name__, static_folder='.', static_url_path='')
        CORS(app)  # Enable CORS for development
        
        # Register all backend blueprints to the main app
        for blueprint in backend_app.blueprints.values():
            app.register_blueprint(blueprint)
        
        # Serve Frontend Static Files
        @app.route('/')
        def serve_index():
            return send_from_directory('.', 'index.html')
        
        @app.route('/<path:path>')
        def serve_static(path):
            if os.path.exists(os.path.join('.', path)):
                return send_from_directory('.', path)
            return send_from_directory('.', 'index.html')

        
        # Health Check
        @app.route('/health')
        def health():
            return jsonify({"status": "healthy", "service": "guideme"})
        
        # Log all requests for debugging
        @app.before_request
        def log_request_info():
            if not request.path.startswith('/js/') and not request.path.startswith('/css/'):
                print(f"📥 Request: {request.method} {request.path}")
        
        print("\n" + "="*60)
        print(f"{Colors.OKGREEN}{Colors.BOLD}🎉 GuideMeAI Server is LIVE!{Colors.ENDC}")
        print("="*60)
        print(f"{Colors.OKCYAN}👉 Open in browser: {Colors.BOLD}http://localhost:5000{Colors.ENDC}")
        print(f"{Colors.OKCYAN}👉 Services: Frontend + API + Chat + Map{Colors.ENDC}")
        print(f"{Colors.OKCYAN}👉 Press Ctrl+C to stop the server{Colors.ENDC}")
        print("="*60 + "\n")
        
        # Run the unified server
        app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
        
    except Exception as e:
        print_error(f"Failed to start server: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    """Main startup routine"""
    print_header("🌏 GuideMeAI - India Local AI Guide")
    
    # Run all checks
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Ollama Service", check_ollama),
        ("Project Structure", check_project_structure),
        ("Port Availability", check_port_availability),
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        if not check_func():
            all_passed = False
            if check_name in ["Python Version", "Dependencies", "Project Structure"]:
                # Critical checks - can't continue
                print_error(f"\n❌ Critical check failed: {check_name}")
                print_info("Please fix the above issues and try again.")
                sys.exit(1)
    
    if not all_passed:
        print_warning("\n⚠️  Some checks failed, but attempting to start anyway...")
        print_info("Note: Chat functionality requires Ollama to be running")
        time.sleep(2)
    else:
        print_success("\n✅ All checks passed!")
        time.sleep(1)
    
    # Start the server
    start_server()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}👋 Server stopped by user{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print_error(f"\n💥 Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
