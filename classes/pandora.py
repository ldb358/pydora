from request import *;
from encoder import *;

import time;
import os;

"""
" This class handles the standard operations of a pandora request
"
"""
class Pandora(object):
    #public vars
    
    #private pandora vars
    __SURL = "https://tuner.pandora.com/services/json/";
    __URL = "http://tuner.pandora.com/services/json/";
    __PARTNER_USERNAME = "android";
    __PARTNER_PASSWORD = "AC7IBG09A3DTSYM4R41UJWL07VLN8JI7";
    __DEVICE = "android-generic";
    __audio_format = "HTTP_64_AACPLUS";
    __partner_id = "";
    __partner_auth ="";
    __user_id = "";
    __user_auth = "";
    __time_offset = 0;
    __test = "";
    __enc = Encoder();
    __station_tokens = list();
    __station_names = list();
    __station_art = list();
    __station_current = None;
    __songs = list();
    __playlist = dict();
    
    
    #Public Methods
    def connect(self):
        args = dict(username = "android", password = "AC7IBG09A3DTSYM4R41UJWL07VLN8JI7", deviceModel = "android-generic", version = "5");
        method = "auth.partnerLogin";
        partnerAuth = self.__send_request(method, args);
        partnerAuth = partnerAuth['result'];
        self.__partner_auth = partnerAuth['partnerAuthToken'];
        self.__partner_id = partnerAuth['partnerId'];
        
        #set the time sync
        sync_time = int(self.__enc.decrypt(partnerAuth['syncTime'])[4:14]);
        self.__time_offset = sync_time - time.time();
        
    def auth(self, user, pswd, webpass):
        if self.__partner_auth == "":
            raise Exception("Partner not signed in cannot continue");
        args = dict(username=user, password=pswd, loginType="user");
        method = "auth.userLogin";
        userAuth = self.__send_request(method, args, True);
        if userAuth != False:
            userAuth = userAuth['result'];
            #'auth.userLogin'
            self.__user_id = userAuth['userId'];
            self.__user_auth = userAuth['userAuthToken'];
            print "User Logged in";
        else:
            raise Exception("User Loggin Failed");
            return;
    
    
    def get_stations(self):
        if self.__user_auth == "":
            raise Exception("User is not authenticated cannot continue");
        method = "user.getStationList";
        args = dict();
        args["includeStationArtUrl"] = True;
        stations = self.__send_request(method, args, True, False);
        stations = stations['result'];
        for i in stations['stations']:
            self.__station_names.append(i['stationName']);
            self.__station_tokens.append(i['stationToken']);
            try:
                self.__station_art.append(i['artUrl']);
            except:
                self.__station_art.append(self.__station_art[0]);
                pass;
        return self.__station_names;
    def get_images(self):
        return self.__station_art;
    def get_playlist(self):
        method = "station.getPlaylist";
        args = dict(stationToken=str(self.__station_tokens[int(self.__station_current)]), additionalAudioUrl=self.__audio_format);
        playlist = self.__send_request(method, args, True, True);
        self.__playlist = playlist['result'];
        
    
    def get_songs(self):
        self.__playlist = 0;
        self.__songs = list();
        #playlist['items'][0]['audioUrlMap']['highQuality']['audioUrl']
        self.get_playlist();
        for song in self.__playlist['items']:
            try:
                song_info = dict(title=song['songName'], artist=song['artistName'], album=song['albumName'], file=song['audioUrlMap']['highQuality']['audioUrl'], albumArt=song["albumArtUrl"]);
                self.__songs.append(song_info);
            except:
                break;
        return self.__songs;
    def set_station(self, stat_id):
        self.__station_current = stat_id;
    #standard getters
    
    
    #private methods
    
    def __send_request(self, method, args = {}, encrypted = False, secure = True):
        if secure:
            req = Request(self.__SURL);
        else:
            req = Request(self.__URL);
        req.addGet('method', method);
        if self.__partner_id:
            req.addGet('partner_id', self.__partner_id);
        if self.__user_id:
            req.addGet('user_id', self.__user_id);
        if self.__user_auth:
            req.addGet('auth_token', self.__user_auth);
        else:
            req.addGet('auth_token', self.__partner_auth);
        enc = Encoder(args);
        
        if self.__time_offset:
            enc.addField('syncTime', int(time.time()+self.__time_offset));
        if self.__partner_auth:
            enc.addField('partnerAuthToken', self.__partner_auth);
        if self.__user_auth:
            enc.addField('userAuthToken', self.__user_auth);
        
        enc.encode(encrypted);
        req.setPost(enc.getEncoded());
        try:
            req.send();
        except Exception as e:
            print "Error: " + e;
        res = req.getResText();
        dec  = Encoder();
        dec.addEncoded(res);
        dec.decode(encrypted);
        data = dec.getDecoded();
        if data['stat'] == 'fail':
            print "\nSo Much Fail So Little Time " + str(data['code']);
            return False;
        return data;        