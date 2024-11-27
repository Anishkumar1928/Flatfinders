from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from firebase import upload_pic,delete_pic


app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Initialize your database class
from RentalAppDB import RentalAppDB
db = RentalAppDB()


@app.route("/")
def home():
    return "app is running"

# Create a route to authenticate your users and return JWTs.
@app.route("/signup", methods=["POST"])
def signup():
    try:
        # Get form data
        name = request.form.get("name")
        mobile = request.form.get("mobile")
        email = request.form.get("email")
        password = request.form.get("password")
        gender = request.form.get("gender")
        role = request.form.get("role")
        profile_pic = request.files.get("file")

        # Check if user already exists
        existing_user = db.read_user(mobile)
        if existing_user:
            return jsonify({"msg": "User already exists."}), 400

        # Upload profile picture if provided
        profile_pic_url = None
        if profile_pic:
            result = upload_pic(profile_pic, "profile_pic", mobile)
            if result["status"] == "error":
                return jsonify({"msg": result["message"]}), 400
            profile_pic_url = result["url"]

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create user
        db.create_user(name, mobile, email, hashed_password, gender, role)
        current_user=db.read_user(mobile)
        
        # Store profile picture URL
        if profile_pic_url:
            db.create_user_profile_pic(current_user[0], profile_pic_url)

        # Create JWT token
        access_token = create_access_token(identity=mobile)
        return jsonify({"access_token": access_token, "profile_pic_url": profile_pic_url}), 201

    except Exception as e:
        print(f"Signup error: {e}")
        return jsonify({"msg": "An error occurred during signup"}), 500


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    mobile = data.get("mobile")
    password = data.get("password")

    # Get user by mobile
    user = db.read_user(mobile) 
    print(user)  # Assume mobile is unique

    if user and check_password_hash(user[4],password):  # Check hashed password
        # Create JWT token
        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad username or password"}), 401


# Update profile route
@app.route("/update_profile", methods=["PUT"])
@jwt_required()
def update_profile():
    current_user = get_jwt_identity()
    user = db.read_user(current_user[2])  # Assuming user_id is the third item in JWT identity
    
    if not user:
        return jsonify({"msg": "User not found."}), 404

    data = request.form.to_dict()

    # Handle profile picture upload
    profile_pic = request.files.get('file')
    if profile_pic:
        filepath = upload_pic(profile_pic, "profile_pic", current_user[2])
        data['profile_pic'] = filepath  # Save image path in the database

    # Update the user profile
    changes = {
        "name": data.get("name"),
        "mobile": data.get("mobile"),
        "email": data.get("email"),
        "gender": data.get("gender"),
        "role": data.get("role")
    }

    db.update_user(user[0], changes)  # Assuming user[0] is the user_id
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
    profilpic=db.read_user_profile_pic(current_user[0])
    return jsonify(logged_in_as=current_user,profilpic=profilpic), 200

# if __name__=='__main__':
#     app.run(debug=True)



