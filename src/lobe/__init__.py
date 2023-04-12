"""Initialize Flask app."""
import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_babel import Babel
from flask_executor import Executor
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy

migrate = Migrate()
security = Security()
db = SQLAlchemy()
babel = Babel()


def add_app_config(app):
    """Add extra configuration to the LOBE app."""
    app.config["DATA_BASE_DIR"] = os.path.join(app.instance_path, "app_data/")
    app.config["TOKEN_DIR"] = os.path.join(app.config["DATA_BASE_DIR"], "tokens/")
    app.config["CUSTOM_TOKEN_DIR"] = os.path.join(app.config["DATA_BASE_DIR"], "custom_tokens/")
    app.config["RECORD_DIR"] = os.path.join(app.config["DATA_BASE_DIR"], "records/")
    app.config["CUSTOM_RECORDING_DIR"] = os.path.join(app.config["DATA_BASE_DIR"], "custom_recordings/")
    app.config["VIDEO_DIR"] = os.path.join(app.config["DATA_BASE_DIR"], "videos/")
    app.config["ZIP_DIR"] = os.path.join(app.config["DATA_BASE_DIR"], "zips/")
    app.config["TEMP_DIR"] = os.path.join(app.config["DATA_BASE_DIR"], "temp/")
    app.config["WAV_AUDIO_DIR"] = os.path.join(app.config["DATA_BASE_DIR"], "wav_audio/")
    app.config["WAV_CUSTOM_AUDIO_DIR"] = os.path.join(app.config["DATA_BASE_DIR"], "wav_custom_audio/")
    app.config["LOG_PATH"] = os.path.join(app.instance_path, "logs", "info.log")
    app.config["OTHER_DIR"] = os.path.join(app.instance_path, "other")
    app.config["STATIC_DATA_DIR"] = os.path.join(app.config["OTHER_DIR"], "static_data/")
    app.config["MANUAL_FNAME"] = "LOBE_manual.pdf"


def create_app():
    from lobe.filters import format_date
    from lobe.forms import ExtendedLoginForm
    from lobe.models import Role, User
    from lobe.views.collection import collection
    from lobe.views.configuration import configuration
    from lobe.views.main import main
    from lobe.views.mos import mos
    from lobe.views.recording import recording
    from lobe.views.session import session
    from lobe.views.token import token
    from lobe.views.user import user
    from lobe.views.verification import verification

    # We need to set the instance path to the location of the config file
    app = Flask(__name__, instance_path=os.environ.get("FLASK_INSTANCE_PATH"), instance_relative_config=True)
    app.config.from_pyfile("config.py")
    add_app_config(app)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(create_logger(app.config["LOG_PATH"]))

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)

    db.init_app(app)
    migrate.init_app(app, db)
    security.init_app(app, user_datastore, login_form=ExtendedLoginForm)
    babel.init_app(app)

    # register filters
    app.jinja_env.filters["datetime"] = format_date

    # Propagate background task exceptions
    app.config["EXECUTOR_PROPAGATE_EXCEPTIONS"] = True
    # register blueprints
    app.register_blueprint(main)
    app.register_blueprint(collection)
    app.register_blueprint(verification)
    app.register_blueprint(token)
    app.register_blueprint(recording)
    app.register_blueprint(session)
    app.register_blueprint(user)
    app.register_blueprint(configuration)
    app.register_blueprint(mos)

    app.executor = Executor(app)
    app.user_datastore = user_datastore

    return app


def create_logger(log_path: str):
    logfile_mode = "w"
    if os.path.exists(log_path):
        logfile_mode = "a"
    else:
        os.makedirs(os.path.split(log_path)[0])
    handler = RotatingFileHandler(log_path, maxBytes=1000, backupCount=1, mode=logfile_mode)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
    return handler
