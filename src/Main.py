import pyglet
import tkinter as tk
import filenameGet
import player
from random import shuffle
from configparser import SafeConfigParser

class App:
    def __init__(self):
        #set up root window
        self.root = tk.Tk()
        self.root.title("Music Player")
        self.root.geometry("300x400")

        #set up pyglet music player
        self.player = player.player()
        self.playing = False
        self.playlist_strings = []

        #images
        self.up = tk.PhotoImage(file='icons\\up.png')
        self.down = tk.PhotoImage(file='icons\\down.png')
        self.delete = tk.PhotoImage(file='icons\\delete.png')
        self.edit = tk.PhotoImage(file='icons\\edit.png')

        #display playlist menu
        self.label_list = tk.Listbox(self.root)
        self.rad_button = tk.Button(self.root,text='randomize',command=self.randomize)
        self.up_button = tk.Button(self.root,height=25,image=self.up,width=30, command = self.move_up)
        self.down_button = tk.Button(self.root,height=25,image=self.down,width=30, command = self.move_down)
        self.delete_button = tk.Button(self.root,height=25,image=self.delete,width=30, command = self.delete_song)
        self.edit_button = tk.Button(self.root,height=25,image=self.edit,width=30, command = self.song_edit)

        self.display_thumbnail = tk.Label(self.root)

        #play pause seek and get song buttons
        self.button_text = tk.StringVar()
        self.playButton = tk.Button(self.root,textvariable=self.button_text,command=self.play_pause)
        self.button_text.set('PLAY')
        self.slider = tk.Scale(self.root,from_=0,to=0,orient='horizontal')
        self.slider.bind("<ButtonRelease-1>",self.updateTime)
        self.slider.bind("<ButtonPress-1>",self.pause)

        #drop down menus
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        #file
        self.file_Menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File",menu=self.file_Menu)
        self.file_Menu.add_command(label="save",command=self.save)
        self.file_Menu.add_command(label="load",command=self.user_load)
        self.file_Menu.add_command(label="Exit",command=self.quit)
        #song getter
        self.get_song_Menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Songs",menu=self.get_song_Menu)
        self.get_song_Menu.add_command(label="song from file",command=self.get_song)

        #volume slider
        self.volume = tk.Scale(self.root,from_=100,to=0,orient='vertical')
        self.volume.bind("<ButtonRelease-1>",self.updateVol)
        self.volume.set(100)

        #packing items
        self.label_list.grid(column=0,row=0)
        self.up_button.grid(column=0,row=2)
        self.down_button.grid(column=0,row=3)
        self.delete_button.grid(column=0,row=4,sticky='n')
        self.edit_button.grid(column=0,row=4,sticky='n',pady=50)
        self.rad_button.grid(column=0,row=1)
        self.slider.grid(column=1,row=3)
        self.display_thumbnail.grid(column=1,row=0)
        self.playButton.grid(column=1,padx=50,row=2)
        self.volume.grid(column=1,row=4)

        #loads default profile
        self.load()

        #update function and main loop
        self.root.after(500,func=self.ping)
        self.root.mainloop()

    def update_playlist(self):
        self.label_list.delete(0,last=self.label_list.size())
        x = 1
        for st in self.playlist_strings:
            self.label_list.insert(x,st)
            x+=1

    def set_playlist_strings(self):
        self.playlist_strings = []
        for song in self.player.playlist:
            self.playlist_strings.append(song.title+'    '+str(round(song.duration)))
        self.update_playlist()

    def move_up(self):
        try:
            copy_playlist = self.player.playlist
            song_id = self.label_list.curselection()[0]
            copy_playlist[song_id],copy_playlist[song_id-1] = copy_playlist[song_id-1],copy_playlist[song_id]
            self.player.set_playlist(copy_playlist)
            self.set_playlist_strings()
        except Exception as e:
            print(str(e)+' move_up')
            return

    def move_down(self):
        try:
            copy_playlist = self.player.playlist
            song_id = self.label_list.curselection()[0]
            copy_playlist[song_id],copy_playlist[song_id+1] = copy_playlist[song_id+1],copy_playlist[song_id]
            self.player.set_playlist(copy_playlist)
            self.set_playlist_strings()
        except Exception as e:
            print(str(e)+' move_down')
            return

    def song_edit(self):
        try:
            song_id = self.label_list.curselection()[0]
            song_to_edit = self.player.playlist[song_id]
            song_to_edit = filenameGet.song_define(path=song_to_edit.path,
                                                    thumbnail=song_to_edit.thumb_path,
                                                    start_time=song_to_edit.start_time,
                                                    end_time=song_to_edit.end_time,
                                                    title=song_to_edit.title)

            song_to_edit = player.song(song_to_edit.path,song_to_edit.end_time,song_to_edit.title,song_to_edit.thumbnail,song_to_edit.start_time)
            copy_playlist = self.player.playlist
            copy_playlist[song_id] = song_to_edit
            self.player.set_playlist(copy_playlist)
            self.set_playlist_strings()
        except Exception as e:
            print(str(e)+' song_edit')
            return

    def delete_song(self):
        try:
            song_id = self.label_list.curselection()[0]
            lb=self.label_list
            lb.delete(tk.ANCHOR)
            copy_playlist=self.player.playlist
            del copy_playlist[song_id]
            curr_song_id = self.player.current_song_id
            self.player.set_playlist(copy_playlist)
            self.player.current_song_id = max(curr_song_id - 1,0)
            self.set_playlist_strings()
            self.update_playlist()
            if len(self.player.playlist) == 0:
                self.playing = False
                self.button_text.set('PLAY')
        except Exception as e:
            print(str(e)+' delete_song')
            return

    def play_pause(self):
        #starting and stoping playback
        if self.player.playing():
            self.player.pause()
            self.playing = False
            self.button_text.set('PLAY')
        else:
            self.player.play()
            self.playing = True
            self.button_text.set('PAUSE')

    def get_song(self):
        #gets new song from file
        args = filenameGet.song_define()
        self.player.load((args.path,args.end_time,args.title,args.thumbnail,args.start_time))
        self.playlist_strings.append(self.player.playlist[len(self.player.playlist)-1].title+'    '+str(round(self.player.playlist[len(self.player.playlist)-1].duration)))
        self.update_playlist()
        if self.player.duration_changed:
            self.slider.config(to=self.player.playlist[self.player.current_song_id].duration)

    def randomize(self):
        songs = self.player.playlist
        if len(songs)>0:
            shuffle(songs)
            self.player.set_playlist(songs)
            del songs
            self.player.duration_changed = True
            self.playlist_strings = []
            for song in self.player.playlist:
                self.playlist_strings.append(song.title+'    '+str(round(song.duration)))
            self.update_playlist()
        else:
            return

    def updateVol(self,event):
        #changes volume
        self.player.volume((1.006956**self.volume.get())-1)

    def updateTime(self,event):
        #sets the song time to the slider
        self.player.seek(self.slider.get())
        if self.playing:
            self.player.play()

    def updateThumbnail(self):
        try:
            img = tk.PhotoImage(file = self.player.playlist[self.player.current_song_id].thumb_path)
            self.display_thumbnail.configure(image=img)
            self.display_thumbnail.image = img
        except Exception as e:
            print(str(e)+' updateThumbnail')
            return

    def pause(self,event):
        self.player.pause()

    def cus_on_eos(self):
        try:
            time = self.player.time() + self.player.playlist[self.player.current_song_id].start_time
            if time > self.player.playlist[self.player.current_song_id].end_time:
                self.player.on_eos()

        except Exception as e:
            print(str(e)+' cus_on_eos')
            return

    def ping(self):
        #general update function
        if self.player.playing():
            if len(self.player.playlist)>0:
                self.slider.set(int(self.player.time()))
                self.cus_on_eos()
        if self.player.duration_changed:
            if self.player.song:
                self.slider.config(to=self.player.playlist[self.player.current_song_id].duration)
                self.updateThumbnail()
                self.player.duration_changed = False
        self.root.after(500,func=self.ping)

    def save(self):
        parser = SafeConfigParser()
        name = 'profiles\\default.ini'
        x = 0
        for song in self.player.playlist:
            parser.add_section('song'+str(x))
            parser.set('song'+str(x),'path',str(song.path))
            parser.set('song'+str(x),'thumb_path',str(song.thumb_path))
            parser.set('song'+str(x),'start_time',str(song.start_time))
            parser.set('song'+str(x),'end_time',str(song.end_time))
            parser.set('song'+str(x),'title',str(song.title))
            x+=1

        with open(name,'w') as f:
            parser.write(f)

    def user_load(self):
        file = filenameGet.getFileName()
        self.load(file)

    def load(self,file = 'profiles\\default.ini'):
        try:
            if file.lower().endswith('.ini'):
                parser = SafeConfigParser()
                parser.read(file)
                songs = []
                for section in parser.sections():
                    path = parser.get(section,'path')
                    end_time = float(parser.get(section,'end_time'))
                    thumb_path = parser.get(section,'thumb_path')
                    start_time = float(parser.get(section,'start_time'))
                    title = parser.get(section,'title')
                    songs.append(player.song(path,end_time,title,thumb_path,start_time))
                self.player.set_playlist(songs)
                del songs
                self.player.duration_changed = True
                self.playlist_strings = []
                for song in self.player.playlist:
                    self.playlist_strings.append(song.title+'    '+str(round(song.duration)))
                self.update_playlist()
            else:
                print('error only ini files supported')
        except Exception as e:
            print(str(e)+' load')
            return

    def quit(self):
        self.root.quit()
        self.root.destroy()
        self.player.quit()

app = App()
