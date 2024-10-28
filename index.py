from wsgi import app
import os

# Check if the database exists before starting the app
if os.path.exists("/tmp/rental_app.db"):
    print("Database file found!")
else:
    print("Database file not found. Creating a new one...")