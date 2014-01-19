from flask import Blueprint, render_template
from flask.views import MethodView
from models import Post
from markdowner import apply_markdown
import datetime
import pytz

blog = Blueprint('blog', __name__)


class List(MethodView):

    def get(self, year=None, month=None, day=None, slug=None, tag=None):
        datestart = datetime.date.min
        dateend = datetime.date.min

        if year:
            datestart = datestart.replace(year=year)
            dateend = dateend.replace(year=year+1)
        if month:
            datestart = datestart.replace(month=month)
            if month == 12:
                dateend = dateend.replace(year=year+1)
                dateend = dateend.replace(month=1)
            else:
                dateend = dateend.replace(month=month+1)
        if day:
            datestart = datestart.replace(day=day)
            one_day = datetime.timedelta(days=1)
            dateend = datestart + one_day

        print datetime.datetime.now()
        print datetime.datetime.utcnow()
        print datetime.datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Singapore'))

        posts = Post.all()\
                    .filter('datecreated >=', datestart)\
                    .filter('datecreated <', dateend)

        return render_template('blog/list.html', posts=posts)


class Detail(MethodView):

    def get(self, year=None, month=None, day=None, slug=None):
        ##print year, month, day, slug
        start_date = datetime.date(year, month, day)
        ##post = Post.all().filter('slug =', slug).get()
        post = Post.all().filter('datecreated >', start_date).get()
        print post
        post.content = apply_markdown(post.content)
        return render_template('blog/detail.html', post=post)

blog.add_url_rule('/blog/', view_func=List.as_view('list_a'))
blog.add_url_rule('/blog/<int:year>/', view_func=List.as_view('list_y'))
blog.add_url_rule('/blog/<int:year>/<int(fixed_digits=2):month>/', view_func=List.as_view('list_ym'))
blog.add_url_rule('/blog/<int:year>/<int(fixed_digits=2):month>/<int(fixed_digits=2):day>/',
                  view_func=List.as_view('list_ymd'))
blog.add_url_rule('/blog/tag/<tag>/', view_func=List.as_view('list_t'))

blog.add_url_rule('/blog/<int:year>/<int(fixed_digits=2):month>/<int(fixed_digits=2):day>/<slug>/',
                  view_func=Detail.as_view('detail_slug'))
blog.add_url_rule('/blog/<slug>', view_func=Detail.as_view('detail'))