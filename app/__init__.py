from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(Config)
CORS(app, supports_credentials=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)


from app.blueprints.api import api

app.register_blueprint(api)

from . import routes, models
