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
        existing_user = db.read_user_mobile(mobile)
        if existing_user:
            return jsonify({"msg": "User already exists."}), 400




        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create user
        db.create_user(name, mobile, email, hashed_password, gender, role)
        current_user=db.read_user_mobile(mobile)

        profile_pic_url = None
        if profile_pic:
            result = upload_pic(profile_pic, "profile_pic", current_user[0])
            if result["status"] == "error":
                return jsonify({"msg": result["message"]}), 400
            profile_pic_url = result["url"]
        
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
    user = db.read_user_mobile(mobile) 
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
     # Assuming user_id is the third item in JWT identity
    user = db.read_user(current_user[0]) 
    
    if not user:
        return jsonify({"msg": "User not found."}), 404

    data = request.form.to_dict()
    print(data)
    print(user)

    # Handle profile picture upload
    profile_pic = request.files.get('file')
   
    print(user[0])
    db.update_user(current_user[0],data) 
    user = db.read_user(current_user[0]) 
    if profile_pic:
        filepath = upload_pic(profile_pic, "profile_pic", user[0])
        print(filepath)
        db.update_user_profile_pic(user[0],filepath) # Assuming user[0] is the
    return jsonify({"msg": "Profile updated successfully."}), 200

@app.route("/delete_user", methods=["DELETE"])
@jwt_required()
def delete_user():
    # Get the current user's mobile from the JWT identity
    current_user = get_jwt_identity()
    # Delete the user from the database
    db.delete_user(current_user[0])  # user[0] is the user_id
    return jsonify({"msg": "User deleted successfully."}), 200


    


# Protect a route with jwt_required, which will kick out requests without a valid JWT present.
@app.route("/getprofile", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    # print(current_user)
    user = db.read_user(current_user[0])
    profilpic=f'https://firebasestorage.googleapis.com/v0/b/flatfinders-3afb3.appspot.com/o/profile_pic%2F{current_user[0]}.jpg?alt=media'
    return jsonify(logged_in_as=user,profilpic=profilpic), 200


@app.route("/addproperty", methods=["POST"])
# @jwt_required()
def addproperty():
    try:
        # current_user=get_jwt_identity()
        # user_id=current_user[0]
        data = request.get_json()
        user_id=11
        property_type = data.get("property_type")
        rent = data.get("rent")
        address = data.get("address")
        Pin_Code = data.get("Pin_Code")
        dimensions = data.get("dimensions")
        accommodation = data.get("accommodation")
        is_occupancy=data.get("is_occupancy")
        is_parking=data.get("is_parking")
        is_kitchen=data.get("is_kitchen")
        # profile_pic = request.files.get("file")   
        
        print(user_id,property_type,rent,address,Pin_Code,dimensions,accommodation,is_occupancy,is_parking,is_kitchen)

        # db.create_property(user_id,property_type,rent,address,Pin_Code,dimensions,accommodation,is_occupancy,is_parking,is_kitchen)
        return jsonify({"msg": "added sucessfully"}),201
    
    except Exception as e:
       print(f"Signup error: {e}")
       return jsonify({"msg": "An error occurred during signup"}), 500
    

@app.route("/getproperty",methods=["POST"])
@jwt_required()
def getproperty():
    data = request.get_json()
    property_id = data.get("property_id")
    try:
        propertydetails = db.read_property(property_id)
        return jsonify(propertydetails=propertydetails), 200
    except Exception as e:
       print(f"propert not found: {e}")
       return jsonify({"msg": "propert not found"}), 500
    


    


