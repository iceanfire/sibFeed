import webapp2



application = webapp2.WSGIApplication([('/push', push),
                                      ('/', HomePage),
                                      ('/feed', Feed),
                                      ('/admin', Admin),
                                      ('/help',Help),
                                      ('/help/(.*)',Help),
                                       ('/resolve/(.*)',Resolve)],
                                     debug=True)

def main():
    application.run()

if __name__ == "__main__":
    main()
