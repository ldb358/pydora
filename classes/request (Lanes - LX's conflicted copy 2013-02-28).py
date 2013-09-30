import re;
import urllib;
import urllib2;
#TODO add post to build, finish the send method
"""
" This class is responsable for building all url requests, sending them and
" Retrieiving the response
"""
class Request(object):
    #public vars
    
    #private vars
    __get = dict(); # a dictionary to hold all get data in an unencoded format
    __post = dict(); # same but for post
    __url = "";
    __return = ""; # the string return from the request
    __usePost = True;
    resText = "";
    #constructor ect

    def __init__(self, url):
        #check if it is a vlid url
        pattern = re.compile("(http)|(https):\/\/.+\.{2,3}$");
        if(re.match(pattern, url)):
            self.__url = url;
        else:
            raise Exception("URL is invlid");
        return;
    
    #Public Methods
    
    """
    " This function builds and sends the request
    " it takes an optional argument for a callback function
    """
    def send(self, callback=0): # this function 
        self.__build();
        if self.__usePost:
            req = urllib2.Request(self.__url, self.__post, {'User-agent': "Mozilla/5.0", 'Content-type': 'text/plain'});
            res = urllib2.urlopen(req);
        else:
            req = urllib2.Request(self.__url);
            res = urllib2.urlopen(req);
        if callback != 0:
            callback(res);
        self.resText = res.read();
        return;
    
    def addPost(self ,key, value=""):
        try:
            dict(key.items() + self.__post.items()); #if key is dictionary merge
        except AttributeError:
            self.__post[key] = value;
        return;
    
    def setPost(self, data):
        self.__post = data;
        
    
    def addGet(self, key, value=""):
        try:
            dict(key.items() + self.__get.items()); #if key is dictionary merge
        except AttributeError:
            self.__get[key] = value;
        return;
    
    #standard getters
    
    def getUrl(self):
        return self.__url;
    
    def getPost(self):
        return self.__post;
    
    def getResText(self):
        return self.resText;
    #private methods
    def tooglePost(self):
        if self.__usePost:
            self.__usePost = False;
        else:
            self.__usePost = True;
    def __build(self): # the function that builds the get and post data
        #first start by building the get parameters
        append = "?";
        for key, value in self.__get.iteritems():
            append += urllib.quote_plus(key)+"="+urllib.quote_plus(value)+"&";
        self.__url += append[0:-1];
        if self.__post == dict(): # post is still empty
            self.__usePost = False;
        #else:
         #   self.__post = urllib.quote_plus(self.__post);
        return;
    
    def clearGet(self):
        self.__get = dict();
    def clearPost(self):
        self.__post = dict();
