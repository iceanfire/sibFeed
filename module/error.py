'''@package
Exceptions related to backend.

@author Peter Cai
'''

class BackEndError(Exception):
    """
    This class represents errors related to backend.
    """

    def __init__(self, msg, response=None):
        """
        Constructor.
        
        msg -- error message.
        """
        self.msg = msg
        self.response = response

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg
