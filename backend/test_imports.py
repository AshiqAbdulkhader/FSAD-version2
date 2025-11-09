#!/usr/bin/env python3
"""Test script to verify all imports work correctly"""

try:
    print("Testing imports...")
    
    # Test Flask and extensions
    from flask import Flask
    from flask_cors import CORS
    from flask_jwt_extended import JWTManager
    print("✓ Flask and extensions imported")
    
    # Test database (will fail if DB not running, but import should work)
    try:
        from config.database import query_db, get_db_connection, return_db_connection
        print("✓ Database module imported")
    except Exception as e:
        print(f"⚠ Database module import issue (expected if DB not running): {e}")
    
    # Test middleware
    from middleware.auth import token_required, role_required, get_current_user
    print("✓ Auth middleware imported")
    
    # Test routes
    from routes import auth, equipment, requests, dashboard
    print("✓ All route modules imported")
    
    # Test app creation (without running)
    from app import app
    print("✓ Flask app created successfully")
    
    print("\n✅ All imports successful!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

