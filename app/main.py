from flask import Flask, send_from_directory, request, jsonify
from app.api.routes import api
import os

app = Flask(__name__, static_folder='static')
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def serve_static():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory('static', path)

# This is for local development only
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000) 