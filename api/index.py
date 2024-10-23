# api/index.py

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Hello from Flask on Vercel!"})

# Export the Flask app as a serverless function
def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)
