# Used to re-calculate help counts
def function initHelpCount():
    for update in statusUpdateListing:
        answersList = answerListing().all().filter('status =',update.key()).order('date').fetch(limit=100)
        update.helpCount = len(answersList)
        update.put()