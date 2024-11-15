import pyrebase
from datetime import datetime
import os


# Load environment variables from .env file

config = {
    "apiKey": "AIzaSyDM3OwPc2E1ArPz3bK3gUJY-vSUWrfIQcs",
    "authDomain": "flatfinders-3afb3.firebaseapp.com",
    "projectId": "flatfinders-3afb3",
    "storageBucket":"flatfinders-3afb3.appspot.com",
    "messagingSenderId": "900610869951",
    "appId":"1:900610869951:web:9513bb6a17e23b417ed40a",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

def upload_profile_pic(image_file, user_id):
    try:
        # Generate unique filename using timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"profile_pics/{user_id}_{timestamp}.jpg"
        
        # Upload file to Firebase Storage
        storage.child(filename).put(image_file)
        
        # Get the URL of uploaded file
        image_url = storage.child(filename).get_url(None)
        print(f"Image uploaded successfully for user {user_id}: {image_url}")
        return image_url

    except Exception as e:
        print(f"Error uploading image for user {user_id}: {str(e)}")
        return None


def delete_profile_pic(image_url):
    try:
        # Extract filename from URL
        filename = image_url.split('/')[-1].split('?')[0]
        
        # Delete file from Firebase Storage
        storage.delete(f"profile_pics/{filename}")
        return True
        
    except Exception as e:
        print(f"Error deleting image: {str(e)}")
        return False

def upload_room_photos(room_id, image_files):
    try:
        image_urls = []
        for image_file in image_files:
            # Generate unique filename using timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"room_photos/{room_id}_{timestamp}.jpg"
            
            # Upload file to Firebase Storage
            storage.child(filename).put(image_file)
            
            # Get the URL of uploaded file
            image_url = storage.child(filename).get_url(None)
            image_urls.append(image_url)
            
        return image_urls
        
    except Exception as e:
        print(f"Error uploading room photos: {str(e)}")
        return None

def delete_room_photo(image_url):
    try:
        # Extract filename from URL
        filename = image_url.split('/')[-1].split('?')[0]
        
        # Delete file from Firebase Storage
        storage.delete(f"room_photos/{filename}")
        return True
        
    except Exception as e:
        print(f"Error deleting room photo: {str(e)}")
        return False

print(config)
