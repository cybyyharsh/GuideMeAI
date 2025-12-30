#!/usr/bin/env python3
"""
Debug server startup script
"""

import sys
import os
sys.path.append('backend')

try:
    print("🚀 Starting Local AI City Agent Server (Debug Mode)")
    print("=" * 50)
    
    # Test imports
    print("📦 Testing imports...")
    
    try:
        from flask import Flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        sys.exit(1)
    
    try:
        from flask_cors import CORS
        print("✅ Flask-CORS imported successfully")
    except ImportError as e:
        print(f"❌ Flask-CORS import failed: {e}")
        sys.exit(1)
    
    try:
        from backend.config import Config
        print("✅ Config imported successfully")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        print("   Creating basic config...")
        
        # Create a basic config if it doesn't exist
        class Config:
            DEBUG = True
            PORT = 5000
    
    try:
        from backend.routes import auth
        print("✅ Auth routes imported successfully")
    except ImportError as e:
        print(f"❌ Auth routes import failed: {e}")
        print("   This might cause auth endpoints to not work")
    
    try:
        from backend.routes import chat, food, traffic, hotels, places
        print("✅ Other routes imported successfully")
    except ImportError as e:
        print(f"❌ Other routes import failed: {e}")
    
    # Create app
    print("\n🏗️  Creating Flask app...")
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['PORT'] = 5000
    
    CORS(app)
    
    # Register health check
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'debug': True}
    
    # Register auth routes manually if import worked
    try:
        from backend.routes.auth import bp as auth_bp
        app.register_blueprint(auth_bp)
        print("✅ Auth routes registered")
    except Exception as e:
        print(f"❌ Failed to register auth routes: {e}")
    
    # Register other routes
    try:
        from backend.routes.chat import bp as chat_bp
        app.register_blueprint(chat_bp)
        print("✅ Chat routes registered")
    except Exception as e:
        print(f"❌ Failed to register chat routes: {e}")
    
    # List all routes
    print("\n📋 Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"   {rule.methods} {rule.rule}")
    
    print(f"\n🌐 Starting server on http://localhost:5000")
    print("   Press Ctrl+C to stop")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
    
except KeyboardInterrupt:
    print("\n👋 Server stopped by user")
except Exception as e:
    print(f"\n💥 Server startup failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)