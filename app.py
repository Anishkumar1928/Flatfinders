from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Initialize your database class
from RentalAppDB import RentalAppDB
db = RentalAppDB()

# Create a route to authenticate your users and return JWTs.
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name")
    mobile = data.get("mobile")
    email = data.get("email")
    password = data.get("password")
    gender = data.get("gender")
    role = data.get("role")

    # Check if user already exists
    existing_user = db.read_user(mobile)  # Assume mobile is unique for simplicity
    if existing_user:
        return jsonify({"msg": "User already exists."}), 400

    # Hash the password before storing it
    hashed_password = generate_password_hash(password)

    # Create a new user
    db.create_user(name, mobile, email, hashed_password, gender, role)

    # Create JWT token
    access_token = create_access_token(identity=mobile)
    return jsonify(access_token=access_token), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    mobile = data.get("mobile")
    password = data.get("password")

    # Get user by mobile
    user = db.read_user(mobile) 
    print(user)  # Assume mobile is unique

    if user and user[4]==password:  # Check hashed password
        # Create JWT token
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad username or password"}), 401


# Update profile route
@app.route("/update_profile", methods=["PUT"])
@jwt_required()
def update_profile():
    # Get the current user's mobile from the JWT identity
    current_user = get_jwt_identity()
    print(current_user)
    user = db.read_user(current_user[2])
    
    if not user:
        return jsonify({"msg": "User not found."}), 404

    data = request.get_json()

    # Create a dictionary for changes
    changes = {
        "name": data.get("name"),
        "mobile": data.get("mobile"),
        "email": data.get("email"),
        "password": generate_password_hash(data.get("password")) if data.get("password") else None,
        "gender": data.get("gender"),
        "role": data.get("role")
    }

    # Update user profile
    db.update_user(user[0], changes)  # user[0] is the user_id
    return jsonify({"msg": "Profile updated successfully."}), 200

@app.route("/delete_user", methods=["DELETE"])
@jwt_required()
def delete_user():
    # Get the current user's mobile from the JWT identity
    current_user = get_jwt_identity()
    user = db.read_user(current_user[2])

    if not user:
        return jsonify({"msg": "User not found."}), 404

    # Delete the user from the database
    db.delete_user(user[0])  # user[0] is the user_id
    return jsonify({"msg": "User deleted successfully."}), 200


    


# Protect a route with jwt_required, which will kick out requests without a valid JWT present.
@app.route("/getprofile", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

