import oauth
import config
import webapp2
import logging

from twitterUser import TwitterUser

from gaesessions import get_current_session

class OauthCallbackHandler(webapp2.RequestHandler):
    def get(self):
        try:
            
            # Check if the validation was denied
            if self.request.get('denied'):
                self.redirect("/?denied=True")
                return
            
            client = oauth.TwitterClient(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.CALLBACK)
            
            authToken = self.request.get("oauth_token")
            authVerifier = self.request.get("oauth_verifier")
            userInfo = client.get_user_info(authToken, auth_verifier=authVerifier)
            
            
            theUserRecord = TwitterUser(
                    key_name = str(userInfo['id']),
                    username = userInfo['username'],
                    accessCode = self.getAccessCodeFromToken(userInfo['token']),
                    accessToken = userInfo['token'],
                    accessSecret = userInfo['secret'])
            
            theUserRecord.put()
            
            session = get_current_session()
            
            session.regenerate_id()
            
            session['twitter_user'] = userInfo
            session['user_record'] = theUserRecord
            
            self.redirect("/builder")
            
        except Exception as e:
            logging.exception(e)
            self.response.clear()
            self.response.set_status(500)
            self.response.out.write("Error validating Twitter's response")

    def getAccessCodeFromToken(self, token):
        return token[-8:]
    
app = webapp2.WSGIApplication([
    ('/oauth_callback', OauthCallbackHandler)
], debug=True)