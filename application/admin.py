from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from auth import requires_auth
from models import Post
from wtforms.ext.appengine.db import model_form
from slugify import slugify

admin = Blueprint('admin', __name__, template_folder='templates')


class List(MethodView):
    decorators = [requires_auth]
    cls = Post

    def get(self):
        posts = self.cls.all()
        return render_template('admin/list.html', posts=posts)


class Detail(MethodView):

    decorators = [requires_auth]

    def get_context(self, slug=None):
        postform = model_form(Post, exclude='slug')

        if slug:
            post = Post.all().filter('slug =', slug).get()
            if request.method == 'POST':
                form = postform(request.form, inital=post._data)
            else:
                form = postform(obj=post)
        else:
            post = Post(title='Untitled', content='Empty', slug='Empty')
            form = postform(request.form)

        context = {
            "post": post,
            "form": form,
            "create": slug is None
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('admin/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            post = context.get('post')
            form.populate_obj(post)
            post.slug = slugify(post.title)
            post.put()

            return redirect(url_for('admin.index'))
        return render_template('admin/detail.html', **context)


# Register the urls
admin.add_url_rule('/admin/', view_func=List.as_view('index'))
admin.add_url_rule('/admin/create/', defaults={'slug': None}, view_func=Detail.as_view('create'))
admin.add_url_rule('/admin/<slug>/', view_func=Detail.as_view('edit'))
