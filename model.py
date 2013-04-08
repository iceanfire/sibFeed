from google.appengine.ext import db


class statusUpdates(db.Model):
    """List of status updates"""
    date = db.DateTimeProperty(auto_now_add=True)
    user = db.UserProperty()
    prefix = db.StringProperty()
    update = db.StringProperty()


class UserProfile(db.Model):
    User = db.UserProperty()
    FirstSession = db.DateTimeProperty(auto_now_add=True)
