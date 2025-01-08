from flask import Flask, jsonify, request,render_template
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from firebase import upload_pic,delete_pic
from datetime import timedelta
from emailsend import send_email
import random
import string



app = Flask(__name__,template_folder="templates")

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit upload size to 16MB
jwt = JWTManager(app)

# Initialize your database class
from RentalAppDB import RentalAppDB
db = RentalAppDB()


@app.route("/")
def home():
    return render_template("index.html")


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

        print(profile_pic_url)
        
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
        access_token = create_access_token(identity=user, expires_delta=timedelta(days=3))
        print("loggedin")
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

@app.route("/update_password", methods=["PUT"])
@jwt_required()
def update_password():
    try:
        # Get the current user's identity from the JWT
        current_user = get_jwt_identity()

        # Fetch the user's details from the database
        user = db.read_user(current_user[0])  # Assuming user[0] is the user_id
        if not user:
            return jsonify({"msg": "User not found."}), 404

        # Get the old password and new password from the request
        data = request.get_json()
        new_password = data.get("new_password")

        # Hash the new password
        hashed_new_password = generate_password_hash(new_password)

        changes={"password": hashed_new_password}

        # Update the password in the database
        db.update_user(current_user[0], changes)

        return jsonify({"msg": "Password updated successfully."}), 200

    except Exception as e:
        print(f"Error updating password: {e}")
        return jsonify({"msg": "An error occurred while updating the password."}), 500


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


@app.route('/property', methods=['POST'])
@jwt_required()
def register_property():
    try:
        current_user = get_jwt_identity()
        # Check incoming request data
        print("Form data:", request.form)
        print("Files:", request.files)

        # Retrieve form data
        property_type = request.form.get('propertyType')
        rent = request.form.get('rent')
        address = request.form.get('address')
        pin_code = request.form.get('pinCode')
        dimensions = request.form.get('dimensions')
        accommodation = request.form.get('accommodation')
        is_parking = request.form.get('isParking') == 'true'
        is_kitchen = request.form.get('isKitchen') == 'true'

        # Validate required fields
        if not property_type or not rent or not address:
            return jsonify({"error": "Missing required fields"}), 400

        # Validate rent and pinCode format
        try:
            rent = float(rent)
            pin_code = int(pin_code)
        except ValueError:
            return jsonify({"error": "Invalid rent or pinCode format"}), 400

        # Handle data upload
        property_id = db.create_property(current_user[0], property_type, rent, address, pin_code, dimensions,
                                         accommodation, True, is_parking, is_kitchen)
        if not property_id:
            return jsonify({"error": "Failed to create property in the database"}), 500

        # Handle image uploads
        images = request.files.getlist('images')
        uploaded_image_urls = []
        if images:
            for index, image_file in enumerate(images):
                result = upload_pic(
                    image_file=image_file,
                    type="property_pic",
                    name=f"{property_id}_{index}"
                )
                if result["status"] == "success":
                    db.create_property_picture(property_id, result["url"])
                    uploaded_image_urls.append(result["url"])
                else:
                    return jsonify({"error": result["message"]}), 500

        # Simulate storing property data
        property_data = {
            "propertyid": property_id,
            "propertyType": property_type,
            "rent": rent,
            "address": address,
            "pinCode": pin_code,
            "dimensions": dimensions,
            "accommodation": accommodation,
            "isParking": is_parking,
            "isKitchen": is_kitchen,
            "images": uploaded_image_urls,
        }
        print(property_id)
        return jsonify({
            "message": "Property registered successfully!",
            "property": property_data
        }), 201

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 400

    


@app.route("/getproperty",methods=["POST"])
@jwt_required()
def getproperty():
    data = request.get_json()
    property_id = data.get("property_id")
    pin_code = data.get("pin_code")
    try:
        if property_id:
            propertydetails = db.read_property(property_id)
            property_photo=db.read_property_picture(property_id)
            return jsonify(propertydetails=propertydetails,property_photo=property_photo), 200
        elif pin_code:
            # Fetch properties based on the given pin code
            propertydetails = db.read_property_pincode(pin_code)

            # Fetch associated property photos for each property
            merged_data = []
            for property_detail in propertydetails:
                property_id = property_detail[0]  # Assuming the first item in the tuple is the property ID
                property_pictures = db.read_property_picture(property_id)
                ownercontact=db.read_user(property_detail[1])[2]
                merged_data.append({
                    "property_details": property_detail,
                    "property_photos": property_pictures,
                    "owner_contact":ownercontact
                })
            return jsonify(merged_data), 200
        else:
            current_user = get_jwt_identity()
            propertydetails = db.read_property_by_id(current_user[0])
            merged_data = []
            for property_detail in propertydetails:
                property_id = property_detail[0]  # Assuming the first item in the tuple is the property ID
                property_pictures = db.read_property_picture(property_id)
                ownercontact=db.read_user(property_detail[1])[2]
                merged_data.append({
                    "property_details": property_detail,
                    "property_photos": property_pictures,
                    "owner_contact":ownercontact
                })
            return jsonify(merged_data), 200
    except Exception as e:
       print(f"propert not found: {e}")
       return jsonify({"msg": "property not found"}), 500
    


@app.route("/deleteproperty",methods=["POST"])
@jwt_required()
def deleteproperty():
    data = request.get_json()
    property_id = data.get("property_id")
    try:
        propertydetails = db.delete_property(property_id)
        return jsonify(msg=propertydetails), 200
    except Exception as e:
       print(f"error: {e}")
       return jsonify({"msg": "Error"}), 500
    


reset_tokens = {}

def generate_reset_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        email = data.get("email")

        # Check if user exists
        user = db.read_user_email(email)
        if not user:
            return jsonify({"msg": "User not found"}), 404

        # Generate a reset token
        token = generate_reset_token()
        reset_tokens[email] = token

        send_email(email,f"Flatfinderapp Reset Token",token)

        return jsonify({"msg": "Password reset token sent to your email."}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"msg": "An error occurred while sending the reset token."}), 500

@app.route('/reset_password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        email = data.get("email")
        token = data.get("token")
        new_password = data.get("new_password")

        # Validate token
        if email not in reset_tokens or reset_tokens[email] != token:
            return jsonify({"msg": "Invalid or expired token."}), 400

        # Update the user's password
        hashed_password = generate_password_hash(new_password)
        changes = {"password": hashed_password}
        db.update_user_email(email, changes)

        # Remove token after successful password reset
        del reset_tokens[email]

        return jsonify({"msg": "Password reset successful."}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"msg": "An error occurred while resetting the password."}), 500
    


    

