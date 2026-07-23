from Config import engine, SessionLocal, Base
from Auth.models import User
from Auth.Sign_up import signup
from flask_cors import CORS
from flask import Flask, jsonify
from Admin.routes import Admin_bp
from Auth.routes import Auth_bp
from Admin.models import Admin
from Department.routes import Department_bp
from Registry.registry_routes import registry_bp
from Notifications.routes import Notification_bp



app = Flask(__name__)
CORS(app, 
     resources={r"/*": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500"]}},
     supports_credentials=True,
     allow_headers=["Content-Type"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)
@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Flask is working'})
@app.before_request
def handle_preflight():
    from flask import request, Response
    if request.method == "OPTIONS":
        res = Response()
        res.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin','*')
        res.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        res.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return res   
app.register_blueprint(Admin_bp, url_prefix="/Admin")
app.register_blueprint(Department_bp, url_prefix="/Department")
app.register_blueprint(Auth_bp, url_prefix="/Auth")
app.register_blueprint(registry_bp, url_prefix="/Registry")
app.register_blueprint(Notification_bp, url_prefix="/Notifications")
def database_init():
    print("Initializing the database...")
    
    db = SessionLocal()
    try:
        Base.metadata.create_all(bind=engine)
        # You can add any initial data seeding here if necessary
        print("Database initialized successfully.")
    except Exception as e:
        print(f"An error occurred during database initialization: {e}")
    db.close()
if __name__ == "__main__":
    database_init()
    app.run(debug=True)
    
            
    