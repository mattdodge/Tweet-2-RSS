import webapp2 as webapp
import os
import jinja2

class FeedEmptyHandler(webapp.RequestHandler):

    def get(self):
        template = jinja_environment.get_template('feedempty.html')
        self.response.out.write(template.render({}))


jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader('view'))

app = webapp.WSGIApplication([('/feed/.*', FeedEmptyHandler)], debug=True)


