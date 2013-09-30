from vlc import *;
"""
" This class encodes the data for transfer for now we will use
" Very specific code with a generic interface for later change
"
"""
class Player(object):
    
    #public vars
    
    #private vars
    __player = "";
    __songs = list();
    __song_loaded = False;
    __oos = None;
    __vplayer = None;
    vlc_event = None;
    __time_callback = False;
    #constructor ect

    def __init__(self):
        self.__vplayer = Instance();
        self.__player = self.__vplayer.media_player_new();
        return;
    
    #Public Methods
    
    def queue(self, song=None):
        if not (song == None):
            self.__songs.append(song);
        else:
            raise Exception("No song passed");
    
    def play(self):
        if len(self.__songs) == 0 and not (self.__oos == None):
            self.__oos();
        if self.__song_loaded:
            self.__player.play();
        else:
            #try:
                Media = self.__vplayer.media_new(unicode(self.__songs[0]['file']));
                self.__player.set_media(Media);
                self.__player.get_media();
                self.__song_loaded = True;
                self.vlc_events = self.__player.event_manager();
                print "Now Playing:", self.__songs[0]["title"], "By", self.__songs[0]["artist"];
                self.__player.play();
            #except:
                #raise Exception("Failed to load song");
        
    def length(self):
        return len(self.__songs);
    
    def pause(self):
        if self.__song_loaded:
            self.__player.pause();
        
    def stop(self):
        if self.__song_loaded:
            #stop playing
            self.__player.stop();
            #remove the first song
            self.__songs.pop(0);
            self.__song_loaded = False;
    
    def ready(self):
        return self.__song_loaded
    
    def skip(self, call=None):
        self.stop();
        self.play();
    #standard getters
    
    def get_title(self):
        return self.__songs[0]["title"];
        
    def get_artist(self):
        return self.__songs[0]["artist"];
    def get_art(self):
        return self.__songs[0]["albumArt"];
        
    def get_album(self):
        return self.__songs[0]["album"];
        
    def song_loaded(self):
        return self.__song_loaded;
    
    def set_time_callback(self, callback):
        self.__time_callback = callback;
    #defs a function to call if songs = 0
    def out_of_songs_callback(self, callback):
        self.__oos = callback;
        
    def get_prog(self):
        return self.__player.get_time();
        
    def get_total(self):
        return self.__player.get_length();
    
    def clear(self):
        self.__songs = list();
        self.__song_loaded = False;
    #private methods
    
"""
vplayer = vlc.Instance();
        player = vplayer.media_player_new();
        Media = vplayer.media_new(unicode(song['file']));
        player.set_media(Media);
       
        player.get_media();
        player.play();
"""