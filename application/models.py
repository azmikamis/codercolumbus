import datetime
import sys

from google.appengine.ext import db

# If the local platform is 64 bit, just using sys.maxint can cause problems.
# It will evaluate to a number that's too large for GAE's 32-bit environment.
# So, force it to a 32-bit number.
FETCH_THEM_ALL = ((sys.maxint - 1) >> 32) & 0xffffffff


class Post(db.Model):
    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    datepublished = db.DateTimeProperty()
    datecreated = db.DateTimeProperty(auto_now_add=True)
    datemodified = db.DateTimeProperty(auto_now=True)







