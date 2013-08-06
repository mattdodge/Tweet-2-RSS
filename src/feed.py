from google.appengine.api import memcache
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
            
            outDict = self.getRSSDictFromTwitterResponse(
                    twitRes, 
                    username + apiEndpoint + urlparse.urlparse(self.request.url).query)
            
            self.response.out.write(xmltodict.unparse(outDict))
            
        except Exception as e:
            logging.exception(e)
            self.raiseError(500, e)
            
    def raiseError(self, errorNum, errorMsg):
        self.response.clear() 
        self.response.set_status(errorNum)
        self.response.out.write(errorMsg)
    
    def getUser(self, username, accessCode):
        # First try memcache
        result = memcache.get(username)

        if result is not None:
            # Did we get a cached result? Use it! 
            return result
        
        # Nothing in cache or expired, fetch from datastore then cache that
        query = TwitterUser.all()
        query.filter("username =", username)
        query.filter("accessCode =", accessCode)
        
        result = query.get()
        
        if not result:
            # Query did not match any access tokens we have, oops
            raise Exception, "No Authorized Twitter User found"

        # Add it to the cache now
        memcache.set(username, result, 60 * 15)
        
        return result
    
    def getParametersDict(self):
        urlInfo = urlparse.urlparse(self.request.url)
        
        params = urlparse.parse_qs(urlInfo.query)
        
        # get rid of the pesky lists that parse_qs produces
        params.update((key, val[0]) for key,val in params.items())
        
        if 'count' not in params:
            params['count'] = 10 
        
        return params
    
    def makeTwitterRequest(self, user, api, params):
        url = "https://api.twitter.com/1.1/{0}".format(api)
        
        client = oauth.TwitterClient(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.CALLBACK)
            
        resp = client.make_request(url, user.accessToken, user.accessSecret, additional_params=params, protected=True)
        
        if resp.status_code == 200:
            return json.loads(resp.content)
        
    def getRSSDictFromTwitterResponse(self, twit, limitKey=None):
        
        limitId = memcache.get(limitKey) if limitKey else None

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
        if not twit:
            logging.warning("We obviously didn't get a valid dictionary")
            # TODO : Probably should do some Twitter error checking here
            twit = []
            
        if 'statuses' in twit:
            twit = twit['statuses']
        
        if not isinstance(twit, list):
            logging.warning("Twitter output should be a list...uh oh")
            twit = []

        # Keep track of the first id, so we can cache it for later
        firstId = twit[0]['id_str'] if len(twit) > 0 and 'id_str' in twit[0] else None

        for tweet in twit:
            try:
                tweet['title'] = tweet['text']
                tweet['description'] = tweet['text']
                tweet['author'] = tweet['user']['screen_name']
                tweet['link'] = 'http://twitter.com/{0}/status/{1}'.format(tweet['author'], tweet['id_str'])
                tweet['guid'] = tweet['id_str']
                tweet['pubDate'] = tweet['created_at']
                
                outItems.append(tweet)

                # Check if we have reached one we've seen before, then kill it
                if limitId and str(limitId) == tweet['id_str']:
                    break

            except Exception as e:
                logging.error("Error processing tweet")
                logging.error(tweet)
                logging.exception(e)
                continue

        if limitKey and firstId and firstId != limitId:
            # Cache the first id we got for this limit key, keep it for 5 mins
            memcache.set(limitKey, firstId, 5 * 60)

        return outDict

app = webapp2.WSGIApplication([('/feed/([a-zA-Z0-9_]{1,15})/([a-zA-Z0-9]+)/?(.*)', FeedHandler)], debug=True)


