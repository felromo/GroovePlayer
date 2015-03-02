import subprocess
import threading
# from __future__ import print_function
# import __future__
from grooveshark import Client

client = Client()
client.init()


class song_listener(threading.Thread):
    """
    Song listener at the moment uses fifo, this functionality should be replaced
    with sockets instead
    """
    def __init__(self, playlist, fifo_path):
        threading.Thread.__init__(self)
        self.fifo_path = fifo_path

    def run(self):
        while True:
            print "waiting for song"
            fifo = open(self.fifo_path, 'r')
            for line in fifo:
                playlist.append(line)
                print line + " appended"
            fifo.close()


class music_player(threading.Thread):
    def __init__(self, playlist):
        threading.Thread.__init__(self)
        self.playlist = playlist

    def run(self):
        while True:
            for play in self.playlist:
                for song in client.search(play, type=Client.SONGS):
                    print(song)
                    subprocess.call(['cvlc', "--play-and-exit", song.stream.url])
                    playlist.pop(0)
                    break


if __name__ == '__main__':
    playlist = []
    path = '/tmp/fifo'
    listener = song_listener(playlist, path)
    player = music_player(playlist)

    listener.start()
    player.start()
