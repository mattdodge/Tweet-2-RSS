Tweet-2-RSS
===========

Convert your Twitter API requests to RSS Feeds
Run on Google App Engine with Python 2.7

http://tweet-2-rss.appspot.com

Sign in with your Twitter and set up RSS feeds in a few seconds.

----

Twitter has removed their v1 API, which allowed for Basic HTTP Authentication. The requirement of OAuth to make API calls has limited other plugins and services from making use of the API the way they used to. In addition, JSON is the only output format supported by the Twitter API now. This service attempts to kill two birds and provide a method to create RSS/XML feeds from the Twitter API.

This repository exists mainly for issue tracking and pull requests, the code gets deployed to GAE to power the service.

-----

## IFTTT

One particularly cool use of this service is that you can now set up Twitter to be a trigger for an IFTTT recipe. IFTTT removed Twitter as a trigger source (though it is still an action) a while back but they do provide RSS feeds as a valid trigger. Set up your RSS feed with Tweet-2-RSS, then get the feed URL for whatever API call you want and use it in your RSS recipe. 

The `author` of each RSS item is the Twitter handle of the tweet, and the `content` and `title` are both the text of the tweet.
