import oauth
import config
import webapp2
import logging

from twitterUser import TwitterUser

class OauthCallbackHandler(webapp2.RequestHandler):
    def get(self):
        try:
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
            
            self.response.out.write(
                """
                    Welcome <b>{0}</b>, you are now connected.<br/>
                    <img src="{1}" />
                    <hr/>
                    Your code is <h2>{2}</h2>
                    <br/><br/>
                    Your feed link will look like <b>http://tweet-2-rss.appspot.com/feed/{3}/{4}</b>
                """.format(
                userInfo['name'], 
                userInfo['picture'],
                self.getAccessCodeFromToken(userInfo['token']),
                userInfo['username'],
                self.getAccessCodeFromToken(userInfo['token'])))
            
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