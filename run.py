from app.main import app

# For Vercel Serverless Functions
from flask import Flask, Request
from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app)

def handler(environ, start_response):
    """Handle WSGI requests."""
    return app.wsgi_app(environ, start_response) 