#!/usr/bin/python
#hello

import logging
import os
from model import *


import webapp2
from google.appengine.api import users # Replace with linkedin?
import jinja2
from module import calltrunk

config = {}
config['webapp2_extras.jinja2'] = {
  'template_path':'/html/',
  'environment_args': {
    'autoescape': True,
    'extensions': [
        'jinja2.ext.autoescape']}
}

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class authHandler(webapp2.RequestHandler):
	def dispatch(self,*args,**kwargs):
		self.user = users.get_current_user()
		userExists = organization.all()
		userExists.filter("user =",self.user).fetch(limit=1)
		
		if not self.user:
			self.redirect(users.create_login_url('/feed'))
		else:
			if userExists.count() == 0:
				self.redirect('/newUser')
			else:
				for userInfo in userExists:
					self.userInfo = {'name':userInfo.name,'phone':userInfo.phone} 

		return super(authHandler, self).dispatch(*args, **kwargs)		

	def render_response(self, template_path, **template_values):
		try:
			template_values['userInfo'] = self.userInfo

			template = jinja_environment.get_template(template_path)
			self.response.write(template.render(**template_values))
		except:
			pass

class HomePage(webapp2.RequestHandler):
	def render_response(self, template_path, **template_values):
		template = jinja_environment.get_template(template_path)
		self.response.write(template.render(**template_values))

	def get(self):
		template_values = {}
		self.render_response('html/home.html', **template_values)

class newUser(webapp2.RequestHandler):
	def render_response(self, template_path, **template_values):
		template = jinja_environment.get_template(template_path)
		self.response.write(template.render(**template_values))

	def get(self):
		template_values = {}
		self.render_response('html/newUser.html', **template_values)
	def post(self):
		newOrganization = organization()
		newOrganization.name = self.request.get('name')
		newOrganization.phone = self.request.get('phone')
		newOrganization.user = self.user = users.get_current_user()
		newOrganization.put()
		self.redirect("/feed")

#@user_required
class Feed(authHandler):
    def get(self):
		user = self.user
		conversationList = conversation.all()
		#conversationList = conversationList.fetch(limit=100)
		conversationList = conversationList.filter("user =", user).fetch(limit=100)
		template_values = {}
		template_values['conversationList'] = conversationList
		#template_values['userInfo'] = self.userInfo
		self.render_response('html/feed.html', **template_values)

class makeCall(authHandler):
	def get(self,sourceNumber):
		#added to make change timeout settings on appengine
		from google.appengine.api import urlfetch
		urlfetch.set_default_fetch_deadline(45)
		logging.info(urlfetch.get_default_fetch_deadline())
		
		#lazy import
		import json
		user = self.user
		sourceNumber = sourceNumber.replace("%2B","+")
		
		#Make Call
		response = calltrunk.makeCall(SourceNumber = sourceNumber)

		conversationId = response['Detail']['ConversationId']
		

		#Add to database
		newConversation = conversation()
		newConversation.user = user
		newConversation.cId = conversationId
		newConversation.put()
		self.redirect('/feed')
		#self.render_resposne('html/feed.html',**template_values)
		#response = calltrunk.makeCall(SourceNumber = '07708087363')

	def post(self,sourceNumber):
		#added to make change timeout settings on appengine
		from google.appengine.api import urlfetch
		urlfetch.set_default_fetch_deadline(45)
		logging.info(urlfetch.get_default_fetch_deadline())
		
		#lazy import
		import json
		
		#Get necessary variables
		user = self.user
		sourceNumber = sourceNumber.replace("%2B","+")
		noteName = self.request.get('noteName')
		
		#Make Call
		response = calltrunk.makeCall(SourceNumber = sourceNumber)
		conversationId = response['Detail']['ConversationId']
		

		#Add to database
		newConversation = conversation()
		newConversation.user = user
		newConversation.cId = conversationId
		newConversation.title = noteName

		newConversation.put()
		self.redirect('/feed')
		#self.render_resposne('html/feed.html',**template_values)
		#response = calltrunk.makeCall(SourceNumber = '07708087363')


class search(authHandler):
	def get(self,query):
		query = self.response.write(query)
		response = calltrunk.search_conversations('this')
		self.response.write(response)

class getConvo(authHandler):
	def get(self,cId):
		response = calltrunk.get_conversation(ConversationId = cId)
		self.response.write(response)

class getRecord(authHandler):
	def get(self,cId):
		response = calltrunk.get_recording(ConversationId = cId)
		self.response.write(response)

application = webapp2.WSGIApplication([('/', HomePage),
									   ('/feed',Feed),
									   ('/makeCall/(.*)',makeCall),
									   ('/newUser',newUser),
									   ('/search/(.*)',search),
									   ('/getConvo/(.*)',getConvo),
									   ('/getRecord/(.*)',getRecord)
									],
                                     debug=True)

def main():
    application.run()

if __name__ == "__main__":
    main()
