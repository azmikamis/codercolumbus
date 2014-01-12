from flask import Blueprint, render_template
from flask.views import MethodView
from models import Post

blog = Blueprint('blog', __name__)


class List(MethodView):

    def get(self):
        posts = Post.all()
        return render_template('posts/list.html', posts=posts)


class Detail(MethodView):

    def get(self, slug):
        post = Post.all().filter('slug =', slug).get()
        return render_template('posts/detail.html', post=post)

blog.add_url_rule('/', view_func=List.as_view('list'))
blog.add_url_rule('/<slug>/', view_func=Detail.as_view('detail'))