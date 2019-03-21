import pyglet
from threading import Thread

class player(object):
    def __init__(self):
        self.playlist = []
        self.current_song_id = 0
        self.player = None
        self.song = None
        self.duration_changed = False
        self.player_thread = Thread(target = self.true_pyglet_loop)
        self.player_thread.start()

    def load(self,args):
        self.playlist.append(song(args[0],args[1],args[2],args[3],args[4]))
        if len(self.playlist)==1:
            self.update()

    def update(self):
        if len(self.playlist)>0:
            playing = self.playing()
            self.pause()
            self.player = None
            self.song = None
            self.player = pyglet.media.Player()
            self.song = pyglet.media.load(self.playlist[self.current_song_id].path)
            self.player.on_eos = self.on_eos
            self.player.queue(self.song)
            self.seek(0)
            if playing:
                self.play()
            if len(self.playlist) - 1 == self.current_song_id:
                self.duration_changed = True
        else:
            self.pause()
            self.player = None
            self.song = None

    def true_pyglet_loop(self):
        pyglet.app.run()

    def time(self):
        if self.song:
            if len(self.playlist)>0:
                return self.player.time-self.playlist[self.current_song_id].start_time
        else:
            return 0

    def on_eos(self):
        if self.current_song_id + 1 == len(self.playlist):
            self.pause()
            self.current_song_id = 0
            return
        else:
            self.current_song_id+=1
            self.update()

    def seek(self,time):
        if self.song:
            if len(self.playlist)>0:
                self.player.seek(max(time+self.playlist[self.current_song_id].start_time,0.0001))
        else:
            return

    def playing(self):
        if self.song:
            return self.player.playing
        else:
            return False

    def volume(self,vol):
        if self.song:
            self.player.volume = vol
        else:
            return

    def set_playlist(self,songs):
        self.pause()
        self.playlist = []
        for s in songs:
            self.playlist.append(s)
        self.current_song_id = 0
        self.update()

    def play(self):
        if self.song:
            self.player.play()
        else:
            return

    def pause(self):
        if self.song:
            self.player.pause()
        else:
            return

    def quit(self):
        self.pause()
        pyglet.app.exit()

class song(object):
    def __init__(self, path, end_time, title, thumb_path, start_time):
        self.path = path
        self.thumb_path = thumb_path
        self.start_time = float(start_time)
        if not(end_time):
            sound = pyglet.media.load(self.path)
            self.end_time = float(sound.duration)
            del sound
        else:
            self.end_time = float(end_time)

        self.duration = self.end_time - self.start_time

        if not(title):
            self.title = self.path.split('/')
            self.title = self.title[len(self.title)-1]
            self.title = self.title.split('.')[0]
        else:
            self.title = title
