'''@package
REST proxy for back-end.

@author Peter Cai
@author Tom Moss
'''
import re
import logging
import urllib2
import json

from error import BackEndError


ERR_BACKEND_NOT_SUPPORT = u"Backend doesn't support this method."

class RestBackEnd(object):
    """
    This class represents a proxy that communicates with Calltrunk backend through REST API.
    """

    def __init__(self, client):
        """
        Constructor.
        """
        self.client = client

    def call_method(self, method_name, **kw):
        try:
            response = self.client.get(method_name, query_args=kw)
            return self.check_response(response)
        except urllib2.URLError, err:
            raise BackEndError(unicode(err))
        
    def call_post_method(self, method_name,jsonData, **kw):
        try:
            response = self.client.post(method_name,kw,jsonData)
            return self.check_response(response)
        except urllib2.URLError, err:
            raise BackEndError(unicode(err))

        
    def upload_file(self, method_name, filename, mimeType, **kw):
        try:
            response = self.client.put(method_name, filename, mimeType, query_args=kw)
            return self.check_response(response)
        except urllib2.URLError, err:
            raise BackEndError(unicode(err))

    def call_list_method(self, method_name, start, size, **kw):
        if start != None:
            kw['Start'] = start
        if size != None:
            kw['Size'] = size

        return self.call_method(method_name, **kw)

    def check_response(self, response):
        '''
        Check response status code.
        '''
        if response.root.get('Status', '') != 'OK':
            raise BackEndError('Error communicating with Calltrunk: %s' % str(response.root['Errors']),
                               response.root)
        return response.root.get('Content', None)
        
    def get_file(self, entity_name, request_headers={}, **kw):
        '''
        Get a file from backend.
        '''
        try:
            return self.client.get_file('Get%s' % entity_name, request_headers, query_args=kw)
        except urllib2.URLError, err:
            raise BackEndError(unicode(err))


class SimpleResponse(object):
    '''
    A simple version of RESTClient.Response, in case that one day I have to
    switch to RESTClient.Response
    '''
    
    def __init__(self, json_text):
        # logging.debug('API returns : %s' % json_text)

        # Handle difference between Python 2.5 and 2.6+
        if hasattr(json, 'loads'):
            self.root = json.loads(json_text)
        else:
            self.root = json.read(json_text)

    def __str__(self):
        return json.dumps(self.root, sort_keys=True, indent=4)

    def __eq__(self, other):
        return self.root == other.root

def build_query(query_dict):
    """
    Build query string from a dictionary.
    
    query_dict -- the dictionary to convert to query string.
    """
    return '&'.join([k + '=' + urllib2.quote(str(v)) for (k,v) in query_dict.items()])
    

class SimpleClient(object):
    """
    A simple version of RESTClient.Client, in case that one day I have to
    switch to RESTClient.Client
    """


    def __init__(self, protocol, server, port, path, authToken):
        """
        Constructor.
        
        server -- backend server IP
        port -- backend server port
        path -- path to API
        """
        self._protocol = protocol
        self._server = urllib2.quote(server)
        self._port = port
        self._path = urllib2.quote(path)
        self._authToken = authToken
        self.base_url = "%s://%s:%d/%s/" % (self._protocol, self._server, self._port, self._path)

    def get(self, path, query_args={}):
        '''
        Get REST response by calling urllib2 APIs.

        path -- relative path to the API
        query_args -- query parameters
        '''
        headers = { 
            'Accept' : 'application/json',
            'X-Authenticator-Session' : self._authToken
            }

        url = self.base_url + urllib2.quote(path) + '/' + (('?' + build_query(query_args)) if len(query_args) > 0 else '')
        req = urllib2.Request(url, headers=headers )
        logging.debug('Call API %s' % url)
        return SimpleResponse(urllib2.urlopen(req).read())
    

    def post(self, path, query_args={},jsonData={}):
        '''
        POST JSON and get REST response by calling urllib2 APIs.

        path -- relative path to the API
        query_args -- query parameters
        jsonData -- json to POST
        '''
        headers = { 
            'Accept' : 'application/json',
            'X-Authenticator-Session' : self._authToken,
            'Content-Type':'application/json'
            }

        url = self.base_url + urllib2.quote(path) + '/' + (('?' + build_query(query_args)) if len(query_args) > 0 else '')
        req = urllib2.Request(url, jsonData, headers=headers)
        logging.debug('Call API %s' % url)
        
        return SimpleResponse(urllib2.urlopen(req).read())
    
    
    def put(self, path, filename, mimeType, query_args={}):
        headers = { 
            'Accept' : 'application/json',
            'X-Authenticator-Session' : self._authToken,
            'Content-Type' : mimeType
            }

        # Python 2.5 doesn't support "with"
        f = open(filename, 'r')
        data = f.read()
        f.close()

        url = self.base_url + urllib2.quote(path) + '/' + (('?' + build_query(query_args)) if len(query_args) > 0 else '')
        req = urllib2.Request(url, headers=headers, data=data)
        req.get_method = lambda: 'PUT'

        return SimpleResponse(urllib2.urlopen(req).read())


    headrs_to_proxy = ["RANGE", 
            "ACCEPT-RANGES", 
            "CONTENT-RANGE", 
            "CONTENT-LENGTH",
            "CONTENT-DISPOSITION",
            ]

    def get_file(self, path, request_headers={}, query_args={}):
        '''
        Get a file back by calling urllib2 APIs.

        path -- relative path to the API
        query_args -- query parameters
        '''
        url = self.base_url + urllib2quote(path) + '/?' + build_query(query_args)

        forward_headers = {}
        for key in self.headrs_to_proxy:
            # Django adds an 'HTTP_' to every HTTP header.
            http_key = 'HTTP_' + key
            if request_headers.has_key(http_key):
                forward_headers[key] = request_headers[http_key]
        req = Request(url, None, forward_headers)
        stream = urllib2.urlopen(req)

        headers = {}
        for header in stream.info().headers:
            m = re.search(r'(\S+):\s*(.+)$', header.strip())
            if m:
                name, value = m.groups()
                if name.upper() in self.headrs_to_proxy:
                    headers[name] = value

        return stream, headers
