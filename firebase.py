import pyrebase
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

def upload_profile_pic(user_id, image_file):
    try:
        # Generate unique filename using timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"profile_pics/{user_id}_{timestamp}.jpg"
        
        # Upload file to Firebase Storage
        storage.child(filename).put(image_file)
        
        # Get the URL of uploaded file
        image_url = storage.child(filename).get_url(None)
        
        return image_url
        
    except Exception as e:
        print(f"Error uploading image: {str(e)}")
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

