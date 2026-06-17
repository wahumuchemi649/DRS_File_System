from Config import engine, SessionLocal, Base
from Auth.models import User
from Auth.Sign_up import signup
from flask_cors import CORS
from flask import Flask, jsonify
from Admin.routes import Admin_bp
from Auth.routes import Auth_bp
from Admin.models import Admin



app = Flask(__name__)
CORS(app, 
     resources={r"/*": {"origins": "http://127.0.0.1:5500"}},
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
        res.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5500'
        res.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        res.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return res   
app.register_blueprint(Admin_bp, url_prefix="/Admin")
app.register_blueprint(Auth_bp, url_prefix="/Auth")
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
    
            
    