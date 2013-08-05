import oauth
import config
import webapp2
import logging

from twitterUser import TwitterUser
from google.appengine.api import urlfetch
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

            if self.request.get('follow'):
                self.followUser(userInfo['token'], userInfo['secret'])

            self.redirect("/builder")
            
        except Exception as e:
            logging.exception(e)
            self.response.clear()
            self.response.set_status(500)
            self.response.out.write("Error validating Twitter's response")

    def getAccessCodeFromToken(self, token):
        return token[-8:]

    def followUser(self, accessToken, accessSecret):
        url = "https://api.twitter.com/1.1/friendships/create.json"
        data = { 'screen_name' : 'Tweet_2_RSS' }

        client = oauth.TwitterClient(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.CALLBACK)
            
        resp = client.make_request(url, accessToken, accessSecret, additional_params=data, method=urlfetch.POST, protected=True)
        
        if resp.status_code == 200:
            return True
        else:
            logging.warning('Unable to follow Tweet_2_RSS : Status {0}'.format(resp.status_code))
            logging.warning(resp)
            return False
    
app = webapp2.WSGIApplication([
    ('/oauth_callback', OauthCallbackHandler)
], debug=True)
