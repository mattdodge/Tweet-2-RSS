import config
import oauth
import webapp2


class TweetConnectHandler(webapp2.RequestHandler):
    def get(self):
        callbackURL = config.CALLBACK + ('?follow=True' if self.request.get('follow') else '')

        client = oauth.TwitterClient(config.CONSUMER_KEY, config.CONSUMER_SECRET, callbackURL)
        
        self.redirect(client.get_authenticate_url())

app = webapp2.WSGIApplication([
    ('/twitter_connect', TweetConnectHandler)
], debug=True)
