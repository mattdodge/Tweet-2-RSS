from twitterUser import TwitterUser
import config
import webapp2 as webapp

class LocalDatastoreCreate(webapp.RequestHandler):
    
    def get(self):
        self.createUser(config.USERNAME, config.TOKEN, config.SECRET)
    
    def createUser(self, username, token, secret):            
        theUserRecord = TwitterUser(
                key_name = str(username),
                username = username,
                accessCode = self.getAccessCodeFromToken(token),
                accessToken = token,
                accessSecret = secret)
        
        theUserRecord.put()
        
    
    def getAccessCodeFromToken(self, token):
        return token[-8:]
    
app = webapp.WSGIApplication([('/localcreate', LocalDatastoreCreate)], debug=True)
    