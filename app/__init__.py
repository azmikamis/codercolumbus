from runutils import fix_sys_path

fix_sys_path()

from flask import Flask
import settings


def register_blueprints(app):
    from views import posts
    from admin import admin
    from test import test
    app.register_blueprint(posts)
    app.register_blueprint(admin)
    app.register_blueprint(test)


app = Flask(__name__)
app.config.from_object(settings)
register_blueprints(app)

