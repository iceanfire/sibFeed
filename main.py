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
from module import email

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
        self.redirect('/feed')


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

        template_values = {'statusUpdates': statusUpdateListing, 'logoutUrl': users.create_logout_url("/")}
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
    def get(self,statusKey):

        answersList = answerListing().all().filter('status =',db.Key(statusKey)).order('date').fetch(limit=100)

        for row in answersList:
            self.response.out.write("<div class='answerWrapper'><span class='user'>"+row.user.nickname()+"</span><span class='answer'>"+row.answer+"</span></div>")
        

    def post(self):
        questionId = int(self.request.get('statusId'))
        questionKey = db.Key.from_path('statusUpdates', questionId)
        newHelp = answerListing()
        newHelp.user = users.get_current_user()
        newHelp.answer = self.request.get('help')

        newHelp.status = statusUpdates.get_by_id(questionId)
        newHelpId = newHelp.put()


        parentQuestion = statusUpdates.get_by_id(questionId)
        parentQuestion.helpCount = parentQuestion.helpCount + 1
        parentQuestion.put()

        answersList = answerListing().all().filter('status =',parentQuestion).order('date').fetch(limit=100)

        # List of all the users who are involved in the thread
        userListing = []
        # Add the people who have answered
        for answer in answersList:
            userListing.append(answer.user)

        # Add the original asker of the question
        userListing.append(parentQuestion.user)

        # Remove duplicates
        userListing = list(set(userListing))

        # Remove the person doing the posting so that he/she doesn't get notified
        try:
            userListing.remove(users.get_current_user())
        except:
            pass
        # Send out the emails

        for user in userListing:
            email.sendNotification(user.email(), 'LearnToDo Notification Update', ""+users.get_current_user().nickname()+" has posted a response to a thread you've signed up for. \r\n\r\nClick here to learn more: \r\nhttp://learntodo.co/feed#"+str(questionKey))

        self.redirect('/feed#'+str(questionKey))

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