import getpass;
import pandora;
import player;
import time;
import gui;
from math import floor;
from Tkinter import *
"""
" This class interacts with the user in order to access pndora
"""
class Ui(object):
    __pan = 0;
    __media = 0;
    Gui = None;
    root = None;
    def __init__(self):
        #step one initilize self.__pandora and get our partner_auth
        self.__pan = pandora.Pandora();
        self.__pan.connect();
        #initilize gui
        root = Tk();
        root.resizable(0, 0);
        self.root = root;
        root.title("Pydora")
        self.Gui = gui.Gui(root);
        self.Gui.set_buttons(self.button_callback);
        self.__media = player.Player();
        self.__media.out_of_songs_callback(self.oos);
        root.after(1000, self.time);
        root.mainloop();
    def oos(self):
        songs = self.__pan.get_songs();
        for song in songs:
            self.__media.queue(song);
    
    def button_callback(self, name):
        buttons = self.Gui.get_buttons();
        textboxes = self.Gui.get_textboxes();
        try:
            user = textboxes['user'].get().strip();
            password = textboxes['pass'].get().strip();
            self.user_login(user, password);
        except:
            if name == "pause":
                self.__media.pause();
                self.Gui.set_buttons(self.button_callback);
                self.media_refresh();
                self.Gui.switch_label('play', 'play');
                self.Gui.set_buttons(self.button_callback);
            elif name == "stop":
                self.__media.stop();
                self.media_refresh();
                self.Gui.switch_label('play', 'play');
                self.Gui.set_buttons(self.button_callback);
            elif name == "play":
                self.__media.play();
                self.Gui.set_buttons(self.button_callback);
                self.media_refresh();
                self.Gui.switch_label('play', 'pause');
                self.Gui.set_buttons(self.button_callback);
            elif name == "skip":
                self.__media.skip();
                self.media_refresh();
                self.Gui.switch_label('play', 'pause');
                self.Gui.set_buttons(self.button_callback);
            elif name == "stations":
                self.stations_refresh();
            else:
                try:
                    stat_id = int(name);
                    self.__pan.set_station(stat_id);
                    songs = self.__pan.get_songs();
                    self.__media.stop();
                    self.__media.clear();
                    for song in songs:
                        self.__media.queue(song);
                    self.media_refresh();
                    self.Gui.switch_label('play', 'pause');
                    self.__media.play();
                except:
                    self.Gui.error("Failed to load station");
    def user_login(self, user, password):
        try:
            self.__pan.auth(user, password);
        except:
            self.Gui.error("Log In Failed");
            return;
        #step three get a station list
        stats = self.__pan.get_stations();
        images = self.__pan.get_images();
        self.Gui.stat_list(stats, self.button_callback, 1,images);
    
    def time(self):
        if self.__media.length() > 0:
            prog = self.__media.get_prog()/1000;
            total = self.__media.get_total()/1000;
            self.__prog = prog;
            pmin = str(prog%60);
            if len(pmin) == 1:
                pmin = "0"+pmin;
            tmin = str(total%60);
            if len(tmin) == 1:
                tmin = "0"+tmin;
            prog = str(int(floor(prog/60)))+ ":" + pmin;
            total = str(int(floor(total/60)))+ ":" + tmin;
            print prog, total
            if prog == total and total != "0:00":
                self.__media.skip();
                self.Gui.media_controls(self.__media.get_art());
                self.Gui.set_buttons(self.button_callback);
                self.Gui.switch_label('play', 'pause');
            self.Gui.error(self.__media.get_title() + " : " + self.__media.get_album() + " - " + self.__media.get_artist() + " (" + str(prog) + "/" + str(total) + ")");
        self.root.after(1000, self.time);
        
    def media_refresh(self):
        self.Gui.media_controls(self.__media.get_art());
        self.Gui.set_buttons(self.button_callback);
        self.Gui.error(self.__media.get_title() + " : " + self.__media.get_album() + " - " + self.__media.get_artist());
    
    def stations_refresh(self):
        stats = self.__pan.get_stations();
        self.Gui.stat_list(stats, self.button_callback,1);
        self.Gui.error("Select a station");