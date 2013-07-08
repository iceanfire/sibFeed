'''
Proxy for back-end.

@author Peter Cai
@author Tom Moss
'''
import logging
import settings
from rest import RestBackEnd, SimpleClient
import unicodedata

def call_method(method_name, **kw):
    '''
    Call a Calltrunk API.
    '''
    return calltrunk_client().call_method(method_name, **kw)

def makeCall(user_id=None,**kw):
	if user_id != None:
		kw['UserId'] = user_id
	
	return calltrunk_client().call_method('MakeCall',**kw)

def get_user(user_id=None):
    '''
    Get the User object from the Calltrunk API.  Returns the current authorized
    user if no user_id is given.
    '''
    kw = { }
    if user_id != None:
        kw['UserId'] = user_id

    return calltrunk_client().call_method('GetUser', **kw)

def update_user(user_id=None,user_json={}):
    '''
    Update the User object with the json data. The json data can be partial
    User data. Updates the current authorized user if no user_id is given.
    '''
    kw = { }
    if user_id != None:
        kw['UserId'] = user_id

    return calltrunk_client().call_post_method('UpdateUser',user_json, **kw)

def get_info(user_id=None):
	kw = {}
	return calltrunk_client().call_method('GetSystemInfo',**kw)

def get_summary(user_id=None):
	kw = {}
	return calltrunk_client().call_method('GetAccountSummarySimple',**kw)

def get_conversation(user_id=None,**kw):
	return calltrunk_client().call_method('GetConversation',**kw)


def create_conversation(user_id=None,trunk_name=None,conv_json={}):
    '''
    Creates a new conversation and returns the conversation object.
    Call this to create a conversation to use with upload_recording and
    index_recordings. The returned conversation will contain a
    ConversationId and TrunkId.
    If no user_id is specified, the current authorized user is assumed.
    If no trunk_name is specified the default trunk for the user is assumed.
    '''
    kw = { }
    if user_id != None:
        kw['UserId'] = user_id
    if trunk_name != None:
        kw['TrunkName'] = trunk_name
        
    return calltrunk_client().call_post_method('CreateConversation',conv_json, **kw)



def upload_recording(conversation_id, filename, trunk_id=None):
    '''
    Upload a WAV audio file to be associated with the specified conversation.
    If no trunk is specified then the current authorized users's trunk is assumed.
    '''
    
    kw = { }

    if trunk_id != None:
        kw['TrunkId'] = trunk_id
    if conversation_id != None:
        kw['ConversationId'] = conversation_id

    return calltrunk_client().upload_file('UploadRecording', filename, 'audio/vnd.wave', **kw)

def get_recording(**kw):
	return calltrunk_client().call_method('GetRecording', **kw)


def index_recordings(conversation_id, trunk_id=None):
    '''
    Index recordings of the specified conversation. Recordings should have
    been previously uploaded with upload_recording.
    If no trunk is specified then the current authorized users's trunk is assumed.
    '''
    kw = { }

    if trunk_id != None:
        kw['TrunkId'] = trunk_id
    if conversation_id != None:
        kw['ConversationId'] = conversation_id

    return calltrunk_client().call_method('IndexRecordings', **kw)

def search_conversations(words,trunk_id=None):
    kw = { }
    kw['Start']=0
    kw['Size'] = 100
    if trunk_id != None:
        kw['TrunkId'] = trunk_id
    if words != None:
        kw['TextQuery'] = words
        
    return calltrunk_client().call_method('SearchConversations', **kw)
    

    
def __normalize_text(text):
    return unicodedata.normalize('NFKD', text).replace(u'\u201c','"').replace(u'\u201d','"').encode('ascii','ignore')

def calltrunk_client():
    """
    Factory function for generating a proxy object which can be used to communicate with the
    back-end.
    """
    return RestBackEnd(
        SimpleClient(settings.CALLTRUNK['PROTOCOL'],
                     settings.CALLTRUNK['HOST'],
                     settings.CALLTRUNK['PORT'],
                     settings.CALLTRUNK['BASE_PATH'],
                     settings.CALLTRUNK['TOKEN']))
