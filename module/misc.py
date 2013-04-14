# Used to re-calculate help counts
def function initHelpCount():
    for update in statusUpdateListing:
        answersList = answerListing().all().filter('status =',update.key()).order('date').fetch(limit=100)
        update.helpCount = len(answersList)
        update.put()

#used to initialize the answered questions
        """for update in statusUpdateListing:
            update.isResolved = False
            update.resolvedBy = None
            update.put()
        
        count = 0
        for update in statusUpdateListing:
          count += 1
          if (count % 2 == 0):
            update.isResolved = True
            update.resolvedBy = users.get_current_user()
            update.put()
          else:
            update.isResolved = False
            update.resolvedBy = users.get_current_user()
            update.put()
          
        """