from runutils import fix_sys_path

fix_sys_path()

import settings
from application import application
from application.blog import blog
from application.admin import admin
from application.test import test

application.config.from_object(settings)
application.register_blueprint(blog)
application.register_blueprint(admin)
application.register_blueprint(test)

app = application

