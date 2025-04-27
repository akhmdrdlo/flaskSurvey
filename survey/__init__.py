from flask import Flask
from survey.routes import survey_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(survey_bp)
    return app
