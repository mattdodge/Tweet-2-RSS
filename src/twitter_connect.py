'''
Created on Jul 2, 2013

@author: matt
'''

import config
import oauth
import webapp2


class TweetConnectHandler(webapp2.RequestHandler):
    def get(self):
        client = oauth.TwitterClient(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.CALLBACK)
        
        self.redirect(client.get_authenticate_url())

app = webapp2.WSGIApplication([
    ('/twitter_connect', TweetConnectHandler)
], debug=True)