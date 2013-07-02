from google.appengine.ext import db

class TwitterUser(db.Model):
    username = db.StringProperty(required=True)
    accessCode = db.StringProperty(required=True)
    accessToken = db.StringProperty(required=True)
    accessSecret = db.StringProperty(required=True)