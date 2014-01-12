from flask import Blueprint, render_template
from flask.views import MethodView
from models import Post

posts = Blueprint('posts', __name__)


class ListView(MethodView):

    def get(self):
        posts = Post.all()
        return render_template('posts/list.html', posts=posts)


class DetailView(MethodView):

    def get(self, slug):
        post = Post.get(slug=slug)
        return render_template('posts/detail.html', post=post)

posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))