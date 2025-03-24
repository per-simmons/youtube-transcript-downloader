from flask import Flask, send_from_directory, request, jsonify
from app.services.transcript_service import get_transcript
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def serve_static():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory('static', path)

@app.route('/api/transcript', methods=['POST'])
def download_transcript():
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
            
        result = get_transcript(url)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# This is important for Vercel
def handler(request):
    """Handle incoming requests."""
    return app(request)

# This is for local development only
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000) 