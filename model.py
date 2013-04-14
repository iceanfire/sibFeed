from google.appengine.ext import db

class organization(db.Model):
    name = db.StringProperty()

class statusUpdates(db.Model):
    """List of status updates"""
    date = db.DateTimeProperty(auto_now_add=True)
    user = db.UserProperty()
    prefix = db.StringProperty()
    update = db.StringProperty()
    orgName = db.ReferenceProperty()


class UserProfile(db.Model):
    User = db.UserProperty()
    FirstSession = db.DateTimeProperty(auto_now_add=True)
    organization = db.ReferenceProperty()

class answerListing(db.Model):
    date = db.DateTimeProperty(auto_now_add=True)
    status = db.ReferenceProperty()
    user = db.UserProperty()
    private = db.BooleanProperty(default=False)
    answer = db.StringProperty()
