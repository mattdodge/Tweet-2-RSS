import webapp2 as webapp
import os
import jinja2

class MainPage(webapp.RequestHandler):
    
    
    def get(self):
        template = jinja_environment.get_template('main.html')
        self.response.out.write(template.render({}))


jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader('view'))

app = webapp.WSGIApplication([('/', MainPage)], debug=True)


