from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def serve_static():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory('static', path)

# This is important for Vercel
def handler(request):
    """Handle incoming requests."""
    return app(request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 