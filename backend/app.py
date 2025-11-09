from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
app.config['CORS_ORIGINS'] = [os.getenv('FRONTEND_URL', 'http://localhost:3000')]

# Initialize JWT
jwt = JWTManager(app)

CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)

# Import routes
from routes import auth, equipment, requests, dashboard

# Register blueprints
app.register_blueprint(auth.bp, url_prefix='/api/auth')
app.register_blueprint(equipment.bp, url_prefix='/api/equipment')
app.register_blueprint(requests.bp, url_prefix='/api/requests')
app.register_blueprint(dashboard.bp, url_prefix='/api/dashboard')

@app.route('/health')
def health():
    return {'status': 'OK', 'message': 'Server is running'}, 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

