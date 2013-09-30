from Tkinter import *
from math import floor;
from PIL import Image, ImageTk;
import urllib2;
import os;
"""
" a class describing the ui using tkinter
"""
class Gui:

    __buttons = dict();
    __textboxes = dict();
    __frame = None;
    __error = object();
    __art = "";
    __callback = False;
    __images = list();
    __can = list();
    can = None;
    yscroll = None;
    embed = None;
    def __init__(self, master):
        self.__frame = Frame(master, borderwidth=5, width=500, height=500);
        self.__frame.grid();
        self.__frame.grid_propagate(0);
        self.__error = Label(self.__frame, text="");
        self.__error.grid(row=0, column=0, columnspan=5);
        self.login_controls();



    def set_button(self, name, callback):
        self.__buttons[name].configure(command=callback);

    def set_buttons(self, callback):
        for name, button in self.__buttons.iteritems():
            button.configure(command= lambda text=button.cget('text'):callback(text));
            self.__callback = callback;

    def media_controls(self, albumArt):
        self.clear();
        if self.__art != albumArt:
            u = urllib2.urlopen(albumArt);
            localFile = open('coverArt-large.jpg', 'wb');
            localFile.write(u.read());
            localFile.close();
            self.__art = albumArt;
        size = 400, 400
        im = Image.open('coverArt-large.jpg')
        im.thumbnail(size, Image.ANTIALIAS)

        tkimage = ImageTk.PhotoImage(im)
        self.__textboxes['albumArt'] = Label(self.__frame, image=tkimage, width=400, height=400);
        self.__textboxes['albumArt'].grid_propagate(0);
        self.__textboxes['albumArt'].grid(row=1, column=0, rowspan=4, columnspan=3)
        self.__textboxes['albumArt'].image = tkimage;
        self.__buttons['play'] = Button(self.__frame);
        self.__buttons['play'].grid(row=5, sticky="nesw");
        self.__buttons['skip'] = Button(self.__frame, text="skip");
        self.__buttons['skip'].grid(row=5, column=1, sticky="nesw");
        self.__buttons['stations'] = Button(self.__frame, text="stations");
        self.__buttons['stations'].grid(row=5, column=2, sticky="nesw");

    def stat_list(self, stats, callback, cols=3, images=list()):
        self.clear();
        count = 0;
        self.yscroll = Scrollbar(self.__frame, orient=VERTICAL);
        self.can = Canvas(self.__frame, width=470, height=465, yscrollcommand=self.yscroll.set, yscrollincrement=10);
        self.can.grid_propagate(0);
        self.embed = Frame(self.can);
        l = (len(images)*50);
        self.can.create_window(235, l,window=self.embed, width=470);
        for i in stats:
            self.__buttons[count] =  Button(self.embed, text=i, command=lambda text=count: callback(text));
            try:
                os.chdir('images');
                file = i.replace('\\', "").replace('/', "").replace(' ', '_').lower();
                if not os.path.isfile(file+'.jpg'):
                    name = file+'.jpg';
                    u = urllib2.urlopen(images[count]);
                    localFile = open(name, 'wb');
                    localFile.write(u.read());
                    localFile.close();
                size =100, 100
                im = Image.open(file+'.jpg');
                im.thumbnail(size, Image.ANTIALIAS);

                tkimage = ImageTk.PhotoImage(im);
                self.__buttons[count] = Frame(self.embed, width=470, height=100);
                self.__buttons[count].grid_propagate(0);
                self.__buttons[count].label =  Button(self.__buttons[count], text=i, command=lambda text=count: callback(text), width=100);
                self.__buttons[count].label.grid_propagate(0);
                self.__buttons[count].label.grid(column=0, row=0);
                self.__images.append(tkimage);
                self.__buttons[count].label.config(image=tkimage);
                self.__buttons[count].text = Button(self.__buttons[count], text=i, command=lambda text=count: callback(text), width=50);
                self.__buttons[count].text.grid_propagate(0);
                self.__buttons[count].text.grid(column=1, row=0, sticky=N+E+S+W);
                os.chdir('../');
            except:
                pass;
            count = count + 1;
        count = 0;
        for name, button in self.__buttons.iteritems():
            r = int(floor(count/cols))+1
            c = int(count%cols);
            count += 1;
            button.grid(row=r, column=c, sticky="nesw");

        for name, text in self.__textboxes.iteritems():
            r = int(floor(count/cols))+1;
            c = int(count%cols);
            count += 1;
            text.grid(row=r, column=c, sticky="nesw");
        r = int(floor(count/cols))+2;
        self.yscroll.config(command=self.can.yview);
        self.yscroll.grid(column=5, row=1, rowspan=4, sticky=N+S);
        self.can.config(scrollregion=(0,0,470,count*110));
        self.can.grid(column=0,row=1, columnspan=4, rowspan=4);
        self.__frame.update_idletasks();
        self.__can.append(self.embed);
        self.__can.append(self.can);
        self.__can.append(self.yscroll);

    def login_controls(self):
        self.clear();
        loginFrame = Frame(self.__frame, padx=110, pady=140);
        self.__textboxes['title'] = Label(loginFrame, text="Welcome To Pydora:");
        self.__textboxes['title'].grid(row=0, column=0, columnspan=2);
        self.__textboxes['user_label'] = Label(loginFrame, text="Username:");
        self.__textboxes['user_label'].grid(row=1, column=0);
        self.__textboxes['pass_label'] = Label(loginFrame, text="Password:");
        self.__textboxes['pass_label'].grid(row=2, column=0);
        self.__textboxes['webpass_label'] = Label(loginFrame, text="Pydora Web Password*:");
        self.__textboxes['webpass_label'].grid(row=3, column=0);
        self.__textboxes['web_tid'] = Label(loginFrame, text="Pydora Web Device ID*:");
        self.__textboxes['web_tid'].grid(row=4, column=0);
        self.__textboxes['web_label'] = Label(loginFrame, text="*All web stuff is optional");
        self.__textboxes['web_label'].grid(row=5, column=0);
        self.__textboxes['user'] = Entry(loginFrame);
        self.__textboxes['user'].grid(row=1, column=1);
        self.__textboxes['pass'] = Entry(loginFrame, show="*");
        self.__textboxes['pass'].grid(row=2, column=1);
        self.__textboxes['webpass'] = Entry(loginFrame, show="*");
        self.__textboxes['webpass'].grid(row=3, column=1);
        self.__textboxes['webtid'] = Entry(loginFrame);
        self.__textboxes['webtid'].grid(row=4, column=1);
        self.__buttons['login'] = Button(loginFrame, text="Login");
        self.__buttons['login'].grid(row=5, column=1, sticky="e")
        loginFrame.grid(row=1);
        self.__can.append(loginFrame);

    def clear(self):
        for name, button in self.__buttons.iteritems():
            button.destroy();
        self.__buttons = dict();
        for name, text in self.__textboxes.iteritems():
            text.destroy();
        self.__textboxes = dict();
        for i in self.__can:
            i.destroy();

    def get_textboxes(self):
        return self.__textboxes;

    def switch_label(self, key, text, type="button"):
        if(type == "button"):
            self.__buttons[key].configure(text=text);
        else:
            self.__textboxes[key].set(text);
        if self.__callback != False:
            self.set_buttons(self.__callback);

    def get_buttons(self):
        return self.__buttons;

    def error(self, message):
        self.__error.config(text=message);
