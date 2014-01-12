from flask import Blueprint, render_template
from flask.views import MethodView

test = Blueprint('test', __name__)


class List(MethodView):

    def get(self):
        return render_template('test/test.html', name='Jack', seq=[1, 2, 3, 4])


test.add_url_rule('/test/', view_func=List.as_view('test'))
