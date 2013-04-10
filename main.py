#!/usr/bin/python
#hello

import logging
import os
from model import *


import webapp2
from google.appengine.api import users #replace with linkedin?
import jinja2
import datetime
from module import time #for time-zone support

config = {}
config['webapp2_extras.jinja2'] = {
  'template_path':'/html/',
  'environment_args': {
    'autoescape': True,
    'extensions': [
        'jinja2.ext.autoescape']}
}

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def user_required(handler):
    """

     """

    def check_login(self, *args, **kwargs):
        pass
        #this handler will take care of checking log-ins in the future.

    return check_login


class authHandler(webapp2.RequestHandler):
    def render_response(self, template_path, **template_values):
        template = jinja_environment.get_template(template_path)
        self.response.write(template.render(**template_values))


class push(webapp2.RequestHandler):
    def post(self):
        pass

    def get(self):
        self.post()


class HomePage(authHandler):
    def get(self):
        template_values = {}
        self.render_response('html/base.html', **template_values)


#@user_required
class Feed(authHandler):
    def get(self):
        user = users.get_current_user()
        userExists = UserProfile.all()
        userExists.filter("User =", user).fetch(limit=1)
        try:
            userExists[0]
        except:
            addNewUser = UserProfile()
            addNewUser.User = user
            addNewUser.put()

        statusUpdateListing = statusUpdates.all().order('-date').fetch(limit=100)
        template_values = {'statusUpdates': statusUpdateListing}
        self.render_response('html/feed.html', **template_values)

    def post(self):
        newStatus = statusUpdates()
        newStatus.prefix = self.request.get('statusPrefix')
        newStatus.update = self.request.get('statusUpdate')
        try:
            newStatus.user = users.get_current_user()
            newStatus.put()
            self.redirect('/feed')
        except:
            self.redirect('/feed')


class Help(authHandler):
    def get(self,statusId):

        searchHelp = answerListing().all().filter('status =',db.Key(statusId)).fetch(limit=100)
        print searchHelp
        for search in searchHelp:
            print search
            #print "<div class='answerWrapper'><span class='user'>"+searchHelp.user.nickname()+"</span><span class='answer'>"+searchHelp.answer+"</span></div>"
        

    def post(self):
        helpAnswer = self.request.get('help')
        helpId = int(self.request.get('statusId'))
        newHelp = answerListing()
        newHelp.user = users.get_current_user()
        newHelp.answer = helpAnswer
        
        newHelp.status = statusUpdates.get_by_id(helpId)
        newHelp.put()

        self.redirect('/feed')

class Admin(authHandler):
    def get(self):
        pass

application = webapp2.WSGIApplication([('/push', push),
                                      ('/', HomePage),
                                      ('/feed', Feed),
                                      ('/admin', Admin),
                                      ('/help',Help),
                                      ('/help/(.*)',Help)],
                                     debug=True)

def main():
    application.run()

if __name__ == "__main__":
    main()