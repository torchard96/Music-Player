import tkinter as tk
from tkinter.filedialog import askopenfilename

def getFileName():
    tk.Tk().withdraw()
    filename = askopenfilename()
    return filename

class song_define(object):
    def __init__(self,path=None,thumbnail=None,start_time=0,end_time=None,title=None):
        self.window = tk.Toplevel()
        self.window.title('get song')

        self.path = path
        self.thumbnail = thumbnail
        self.start_time = start_time
        self.end_time = end_time
        self.title = title

        self.title_label = tk.Label(self.window,text='Enter Song Title')
        self.title_entry = tk.Entry(self.window)
        if self.title:
            self.title_entry.insert(0,self.title)
        self.get_song_text = tk.StringVar()
        self.get_song = tk.Button(self.window,textvariable=self.get_song_text,command = self.browse_song)
        self.get_song_text.set('browse for song*')
        if self.path:
            self.get_song_text.set(self.path)

        self.start_time_label = tk.Label(self.window,text='enter start time (not required)')
        self.end_time_label = tk.Label(self.window,text='enter end time (not required)')
        self.start_time_entry = tk.Entry(self.window)
        if not(self.start_time) == 0:
            self.start_time_entry.insert(0,str(self.start_time))
        self.end_time_entry = tk.Entry(self.window)
        if self.end_time:
            self.end_time_entry.insert(0,str(self.end_time))

        self.thumbnail_label = tk.Label(self.window,text='Thumbnail')
        self.get_thumbnail_text = tk.StringVar()
        self.get_thumbnail = tk.Button(self.window,textvariable=self.get_thumbnail_text,command = self.browse_thumbnail)
        self.get_thumbnail_text.set('browse for Thumbnail (not required)')
        if self.thumbnail:
            self.get_thumbnail_text.set(self.thumbnail)
        self.thumbnail_display = tk.Label(self.window)

        self.load_song = tk.Button(self.window,text='load song',command = self.return_song)

        self.title_label.grid(column=0,columnspan=20,row=0)
        self.title_entry.grid(column=0,columnspan=20,row=1)
        self.get_song.grid(column=0,columnspan=20,row=2)
        self.start_time_label.grid(column=0,row=3,sticky='w')
        self.end_time_label.grid(column=1,row=3,sticky='e')
        self.start_time_entry.grid(column=0,row=5)
        self.end_time_entry.grid(column=1,row=5)
        self.thumbnail_label.grid(column=0,columnspan=20,row=6)
        self.get_thumbnail.grid(column=0,columnspan=20,row=7)
        self.thumbnail_display.grid(column=0,columnspan=20,row=8)
        self.load_song.grid(column=0,columnspan=20,row=9)

        self.window.mainloop()

    def browse_song(self):
        self.path = getFileName()
        if self.path.lower().endswith(('.au','.mp2','.mp3','.ogg','.wav',',wma','mp4')):
            self.get_song_text.set(self.path)
        else:
            self.path = None
            print('error invaild file type')

    def browse_thumbnail(self):
        self.thumbnail = getFileName()
        try:
            self.img = tk.PhotoImage(file = self.thumbnail)
            self.thumbnail_display.configure(image=self.img)
        except Exception as e:
            print(str(e)+' browse_thumbnail')
            print('error loading thumbnail')

    def return_song(self):
        if self.path:
            try:
                self.title = self.title_entry.get()
                if len(self.title) == 0:
                    self.title = None
            except:
                self.title = None
            try:
                self.end_time = self.end_time_entry.get()
                if len(self.end_time) == 0:
                    self.end_time = None
            except:
                self.end_time = None
            try:
                self.start_time = self.start_time_entry.get()
                if len(self.start_time) == 0:
                    self.start_time = 0
            except:
                self.start_time = 0

            self.window.quit()
            self.window.destroy()
