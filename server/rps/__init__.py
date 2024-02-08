from flask import Flask
from flask_caching import Cache
import os

cache = Cache()
db = SQLAlchemy()


dbname = (os.environ.get("DB_NAME"),)
user = (os.environ.get("DB_USER"),)
password = (os.environ.get("DB_PASSWORD"),)
host = (os.environ.get("DB_HOST"),)
port = (os.environ.get("DB_PORT"),)

# DATABASE_USER:PASSWORD@DATABASE_HOST_NAME:DATABASE_PORT/DATABASE_NAME
db_conn_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"


def create_app(test_config=None):
    from . import models

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=db_conn_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        CACHE_TYPE="FileSystemCache",
        CACHE_DIR=os.path.join(app.instance_path, "cache"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        db.init_app(app)
        db.create_all()
        cache.init_app(app)

    app.cli.add_command(models.init_db_command)
    app.cli.add_command(models.populate_db_command)

    return app
