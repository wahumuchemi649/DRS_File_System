from flask import Blueprint, request, jsonify
from Auth.Sign_up import signup
from Auth.models import User
from Auth.login import login

Auth_bp = Blueprint('Auth', __name__)

@Auth_bp.route('/signup', methods=['POST'])
def signup_route():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400
    user = User(
        firstName=data.get('firstName'),
        lastName=data.get('lastName'),
        email=data.get('email'),
        password=data.get('password'),
        roles=data.get('role'),
        deptId=data.get('deptId')
    )
    result = signup(user)
    if 'error' in result:
        return jsonify(result), 400
    return jsonify(result), 201


@Auth_bp.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400
    result = login(data.get('email'), data.get('password'))
    if 'error' in result:
        return jsonify(result), 401
    return jsonify(result), 200