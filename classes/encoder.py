import json;
from includes.blowfish import *;
from includes.keys import *;
"""
" This class encodes the data for transfer for now we will use
" Very specific code with a generic interface for later change
"
"""
class Encoder(object):
    
    #public vars
    
    #private vars
    PREV = "";
    __varibles = {};
    __output = "";
    __input = {};
    blowfish_decode = Blowfish("R=U!LH$O2B#");
    blowfish_encode = Blowfish("6#26FRL$ZWD");
    #constructor ect

    #pass a dict data to be encoded
    def __init__(self, data={}, prev=PREV):
        self.__input = data;
        return;
    
    #Public Methods
    def addField(self, key, value):
        try:
            dict(key.items() + self.__input.items()); #if key is dictionary merge
        except AttributeError:
            self.__input[key] = value;
        return;
    #encode the data into json, if blowfish is true
    #encrypt it using blow fish and the password
    def encode(self, blowfish=False):
        jsoned = json.dumps(self.__input);
        encrypted = "";
        if blowfish:
            encrypted = self.__pandora_encrypt(jsoned);
        else:
            encrypted = jsoned;
        self.__output = encrypted;
        return;
    #decode the encrypted data
    def decode(self, blowfish = False):
        decrypted = "";
        if blowfish:
            try:
                decrypted = self.__pandora_decrypt(self.__output);
            except TypeError:
                decrypted = self.__output;
        else:
            decrypted = self.__output;
        self.__input = json.loads(decrypted);
        return;
    
    #decrypts blowfist for a string(for time sync particularly)
    def decrypt(self, data):
        return self.__pandora_decrypt(data);
    
    def addEncoded(self, encoded):
        self.__output = encoded;
    #standard getters
    def getEncoded(self):
        return self.__output;
    
    def getDecoded(self):
        return self.__input;
    #private methods
    def __pad(self, s, l):
        return s + "\0" * (l - len(s))
    
    def __pandora_encrypt(self, s):
        return "".join([self.blowfish_encode.encrypt(self.__pad(s[i:i+8], 8)).encode('hex') for i in xrange(0, len(s), 8)]);
    
    
    
    def __pandora_decrypt(self, s):
        return "".join([self.blowfish_decode.decrypt(self.__pad(s[i:i+16].decode('hex'), 8)) for i in xrange(0, len(s), 16)]).rstrip('\x08')
        
        