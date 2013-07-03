import webapp2
from twitterUser import TwitterUser
import oauth
import config
import logging
import urlparse
try:
    import json
except:
    from django.utils import simplejson as json
    
import xmltodict

class FeedHandler(webapp2.RequestHandler):

    def get(self, username, accessCode, apiEndpoint=None):
        try:
            self.response.headers['Content-Type'] = 'application/rss+xml'
        
            if not apiEndpoint:
                apiEndpoint = "statuses/home_timeline.json"
            
            twitRes = self.makeTwitterRequest(
                user = self.getUser(username, accessCode), 
                api = apiEndpoint, 
                params = self.getParametersDict())
            
#             self.response.out.write(json.dumps(twitRes))
#             
#             self.response.out.write("\n\n\n")
            
            outDict = self.getRSSDictFromTwitterResponse(twitRes)
            
            self.response.out.write(xmltodict.unparse(outDict))
            
        except Exception as e:
            logging.exception(e)
            self.response.clear()
            self.response.set_status(500)
            self.response.out.write(e)
    
    def getUser(self, username, accessCode):
        query = TwitterUser.all()
        query.filter("username =", username)
        query.filter("accessCode =", accessCode)
        
        result = query.get()
        
        if not result:
            # Query did not match any access tokens we have, oops
            raise Exception, "No Authorized Twitter User found"
        
        return result
    
    def getParametersDict(self):
        urlInfo = urlparse.urlparse(self.request.url)
        
        params = urlparse.parse_qs(urlInfo.query)
        
        # get rid of the pesky lists that parse_qs produces
        params.update((key, val[0]) for key,val in params.items())
        
        return params
    
    def makeTwitterRequest(self, user, api, params):
        url = "https://api.twitter.com/1.1/{0}".format(api)
        
        client = oauth.TwitterClient(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.CALLBACK)
            
        resp = client.make_request(url, user.accessToken, user.accessSecret, additional_params=params, protected=True)
        
        if resp.status_code == 200:
            return json.loads(resp.content)
        
    def getRSSDictFromTwitterResponse(self, twit):
        outDict = {
            'rss' : {
                '@version' : '2.0',
                'channel' : {
                    'title' : 'Tweet 2 RSS Feed',
                    'description' : 'Converting Twitter API Queries to RSS',
                    'link' : 'http://tweet-2-rss.appspot.com',
                    'item' : []
                }
            }
        }
        
        outItems = outDict['rss']['channel']['item']
        
        for tweet in twit:
            tweet['title'] = tweet['text']
            tweet['description'] = tweet['text']
            tweet['author'] = tweet['user']['screen_name']
            tweet['link'] = 'http://twitter.com/{0}/status/{1}'.format(tweet['author'], tweet['id_str'])
            tweet['guid'] = tweet['id_str']
            tweet['pubDate'] = tweet['created_at']
            
            outItems.append(tweet)
        
        return outDict

app = webapp2.WSGIApplication([('/feed/([a-zA-Z0-9_]{1,15})/([a-zA-Z0-9]+)/(.*)', FeedHandler)], debug=True)


