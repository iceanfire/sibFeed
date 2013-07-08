from google.appengine.ext import db


class conversation(db.Model):
	user = db.UserProperty()
	cId = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	title = db.StringProperty()

class organization(db.Model):
    user = db.UserProperty()
    name = db.StringProperty()
    phone = db.StringProperty()
    dateCreated = db.DateTimeProperty(auto_now_add=True)

class statusUpdates(db.Model):
	"""List of status updates"""
	date = db.DateTimeProperty(auto_now_add=True)
	user = db.UserProperty()
	prefix = db.StringProperty()
	update = db.StringProperty()
	helpCount = db.IntegerProperty(default=0)
	orgName = db.ReferenceProperty()
	isResolved = db.BooleanProperty(default=False)
	resolvedBy = db.UserProperty()
	location = db.StringProperty()


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
