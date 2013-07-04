import webapp2 as webapp
import os
import jinja2

from gaesessions import get_current_session
import logging

class BuilderHandler(webapp.RequestHandler):
    
    def get(self):
        template = jinja_environment.get_template('builder.html')

        session = get_current_session()
        
        twitterUser = session.get('twitter_user')
        userRecord = session.get('user_record')
        
        if not (session.is_active() and twitterUser and userRecord):
            logging.warning("Builder was accessed with no session variable")
            self.redirect("/twitter_connect")
            return
         
        self.response.out.write(template.render({
                'twitterUser' : twitterUser,
                'userRecord' : userRecord
        }))
           

jinja_environment = jinja2.Environment(
    autoescape=True,
    loader=jinja2.FileSystemLoader('view'))

app = webapp.WSGIApplication([('/builder', BuilderHandler)], debug=True)


