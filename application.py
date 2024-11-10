from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()


def create_app(**config_overrides):
    app = Flask(__name__)

    # Load config
    app.config.from_pyfile('settings.py')

    db.init_app(app)
    migrate = Migrate(app, db)

    #importing apps
    from admin.views import admin_app
    from user.views import user_app

    #registering blueprints
    app.register_blueprint(user_app)
    app.register_blueprint(admin_app)
    return app
