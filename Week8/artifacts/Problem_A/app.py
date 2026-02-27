"""
Flask app entry point.
Creates the app, registers blueprints, and runs the server.
"""
from flask import Flask
from webhook.views import webhook_bp

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.register_blueprint(webhook_bp, url_prefix="")
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
