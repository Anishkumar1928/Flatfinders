import pyrebase
import os
# Firebase configuration
config = {
    "apiKey": "AIzaSyDM3OwPc2E1ArPz3bK3gUJY-vSUWrfIQcs",
    "authDomain": "flatfinders-3afb3.firebaseapp.com",
    "projectId": "flatfinders-3afb3",
    "storageBucket": "flatfinders-3afb3.appspot.com",
    "messagingSenderId": "900610869951",
    "appId": "1:900610869951:web:9513bb6a17e23b417ed40a",
    "databaseURL": "",
    "serviceAccount": os.path.join(os.getcwd(), "serviceAccountKey.json")
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
storage = firebase.storage()

# Function to upload a profile picture to Firebase Storage
def upload_pic(image_file, type, name):
    try:
        # Generate unique filename
        filename = f"{type}/{name}.jpg"
        
        # Read the image file into bytes
        image_data = image_file.read()  # Read the file content as bytes
        
        # Upload the file to Firebase Storage
        storage.child(filename).put(image_data, token=None)

        # Get the URL of the uploaded file
        image_url = storage.child(filename).get_url(token=None)
        print(f"Image uploaded successfully for user {name}: {image_url}")
        return {"status": "success", "url": image_url}
    except Exception as e:
        error_msg = f"Error uploading image for user {name}: {str(e)}"
        print(error_msg)
        return {"status": "error", "message": error_msg}


# Function to delete a profile picture from Firebase Storage
def delete_pic(storage_path):
    try:
        storage.delete(storage_path, None)
        print(f"Image deleted successfully from path: {storage_path}")
        return True
    except Exception as e:
        print(f"Error deleting image: {e}")
        return False



# Example usage
if __name__ == "__main__":
    # print(storage.child("yoyo").child("yoyo.jpeg").put("yoyo.jpeg"))
    #storage.delete("yoyo/yoyo.jpeg", None)
    print(upload_pic("yoyo.jpeg","yoyo","12i4"))
    # delete_pic("12i4.jpg")
    # print(os.getcwd())
