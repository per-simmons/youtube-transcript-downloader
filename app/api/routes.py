from flask import Blueprint, jsonify, request, abort
from app.services.transcript_service import get_transcript

api = Blueprint('api', __name__)

@api.route('/transcript', methods=['POST'])
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