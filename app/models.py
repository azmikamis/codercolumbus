import datetime
import sys

from google.appengine.ext import db

# If the local platform is 64 bit, just using sys.maxint can cause problems.
# It will evaluate to a number that's too large for GAE's 32-bit environment.
# So, force it to a 32-bit number.
FETCH_THEM_ALL = ((sys.maxint - 1) >> 32) & 0xffffffff


class Article(db.Model):
    title = db.StringProperty(required=True)
    body = db.TextProperty()
    published_when = db.DateTimeProperty(auto_now_add=True)
    tags = db.ListProperty(db.Category)
    pk = db.StringProperty()
    draft = db.BooleanProperty(required=True, default=False)

    @classmethod
    def get_all(cls):
        q = db.Query(Article)
        q.order('-published_when')
        return q.fetch(FETCH_THEM_ALL)

    @classmethod
    def get(cls, pk):
        q = db.Query(Article)
        q.filter('id = ', pk)
        return q.get()

    @classmethod
    def published_query(cls):
        q = db.Query(Article)
        q.filter('draft = ', False)
        return q

    @classmethod
    def published(cls):
        return Article.published_query().order('-published_when').fetch(FETCH_THEM_ALL)

    def save(self):
        previous_version = Article.get(self.id)
        try:
            draft = previous_version.draft
        except AttributeError:
            draft = False

        if draft and (not self.draft):
            # Going from draft to published. Update the timestamp.
            self.published_when = datetime.datetime.now()

        try:
            obj_id = self.key().id()
            resave = False
        except db.NotSavedError:
            # No key, hence no ID yet. This one hasn't been saved.
            # We'll save it once without the ID field; this first
            # save will cause GAE to assign it a key. Then, we can
            # extract the ID, put it in our ID field, and resave
            # the object.
            resave = True

        self.put()
        if resave:
            self.pk = self.key().id()
            self.put()





