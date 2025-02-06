from flask import Flask, jsonify, request
import jwt
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)
SECRET_KEY = 'your_secret_key'

users = [
    {"id": 1, "name": "Emma Watson", "email": "emma.w@example.com", "role": "Admin"},
    {"id": 2, "name": "Liam Johnson", "email": "liam.j@example.com", "role": "User"},
    {"id": 3, "name": "Sophia Martinez", "email": "sophia.m@example.com", "role": "User"},
    {"id": 4, "name": "Noah Williams", "email": "noah.w@example.com", "role": "User"},
    {"id": 5, "name": "Olivia Brown", "email": "olivia.b@example.com", "role": "User"}
]

def generate_token(user_id, role):
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode(
        {'user_id': user_id, 'role': role, 'exp': expiration},
        SECRET_KEY,
        algorithm='HS256'
    )
    return token

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            token = token.split(" ")[1]
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        return f(decoded, *args, **kwargs)
    return decorated_function

def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(decoded, *args, **kwargs):
            if decoded['role'] != role:
                return jsonify({'message': 'You do not have permission to access this resource'}), 403
            return f(decoded, *args, **kwargs)
        return decorated_function
    return wrapper

@app.route("/api/GetUsers", methods=["GET"])
@token_required
@role_required("Admin")
def get_users(decoded):
    return jsonify(users)

@app.route("/api/PostUsers", methods=["POST"])
@token_required
def create_user(decoded):
    new_user = request.json
    new_user["id"] = max([u["id"] for u in users], default=0) + 1
    users.append(new_user)
    return jsonify(new_user), 201

@app.route("/api/PatchUsers/<int:user_id>", methods=["PATCH"])
@token_required
def update_user(decoded, user_id):
    for user in users:
        if user["id"] == user_id:
            user.update(request.json)
            return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route("/api/DeleteUsers/<int:user_id>", methods=["DELETE"])
@token_required
@role_required("Admin")
def delete_user(decoded, user_id):
    global users
    user_to_delete = next((u for u in users if u["id"] == user_id), None)
    if user_to_delete:
        users = [u for u in users if u["id"] != user_id]
        return jsonify({"message": "User deleted"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route("/api/login", methods=["POST"])
def login():
    auth = request.json
    user_email = auth.get("email")
    user_password = auth.get("password")
    for user in users:
        if user['email'] == user_email:
            token = generate_token(user['id'], user['role'])
            return jsonify({"token": token})

    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(debug=True)