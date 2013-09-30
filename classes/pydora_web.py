from request import *;
from encoder import *;
import urllib;

"""
" This class handles the standard operations of a pydora request
"
"""
class Pydora_Web(object):
    
    #private pydora web vars
    __URL = "http://lanedev.dyndns.org/pydora_drupal/api";
    __pydora_auth_token = 0;
    __device_id = 0;
    __enc = Encoder();
    __enabled = False;
    __username = 0;
    
    def auth(self, username, password):
        args = dict(username=username, password=password);
        worked = self.__send_pydora_web_request("validate", args);
        if int(worked) != 0:
            print "User Logged In to Pydora Web"
            self.__pydora_auth_token = worked;
            self.__username = username;
        else:
            print "Pydora Web Login Failed";
            
    def add_device(self, device_id):
        args = dict(username=self.__username, auth_id=self.__pydora_auth_token, device=device_id);
        worked = self.__send_pydora_web_request("add_device", args);
        if int(worked) != 0:
            print "Device Added With ID", worked
            self.__device_id = worked;
            self.__enabled = True;
        else:
            print "Failed to add device";
    
    def get_commands(self):
        args = dict(username=self.__username, auth_id=self.__pydora_auth_token, device=self.__device_id);
        worked = self.__send_pydora_web_request("get_queue", args);
        if worked.strip() != "0":
            print "Commands Recieved:", worked
            return worked.split(",");
        else:
            print "No Current Commands";
            return [];
            
    def clear_commands(self):
        args = dict(username=self.__username, auth_id=self.__pydora_auth_token, device=self.__device_id);
        worked = self.__send_pydora_web_request("clear_queue", args);
        if worked.strip() == "0":
            print "Commands Cleared"

    def __send_pydora_web_request(self, method, args = {}):
        req = Request(self.__URL+"/"+method);
        enc = Encoder(args);
        if self.__pydora_auth_token != 0:
            enc.addField('userAuthToken', self.__pydora_auth_token);
        req.addGet('method', method);
        enc.encode(False);
        req.setPost(enc.getEncoded());
        try:
            req.send();
        except Exception as e:
            print "Error: " + str(e);
        res = req.getResText();
        return res.strip();

    #tells the program whether or not to check for
    # online commands ie. the device has been registered
    def enabled(self):
        return self.__enabled;