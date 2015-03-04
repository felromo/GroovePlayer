import subprocess
import threading
import time
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
    def __init__(self, playlist, fifo_path, run_event):
        threading.Thread.__init__(self)
        self.fifo_path = fifo_path
        self.run_event = run_event

    def run(self):
        while self.run_event.is_set():
            print "waiting for song"
            fifo = open(self.fifo_path, 'r')
            for line in fifo:
                playlist.append(line)
                print line + " appended"
            fifo.close()


class music_player(threading.Thread):
    def __init__(self, playlist, run_event):
        threading.Thread.__init__(self)
        self.playlist = playlist
        self.run_event = run_event

    def run(self):
        while self.run_event.is_set():
            time.sleep(5)
            for play in self.playlist:
                for song in client.search(play, type=Client.SONGS):
                    print(song)
                    subprocess.call(['cvlc', "--play-and-exit", song.stream.url])
                    playlist.pop(0)
                    break


if __name__ == '__main__':
    playlist = []
    path = '/tmp/fifo'
    fifo_interrupt = None
    run_event = threading.Event()
    run_event.set()
    listener = song_listener(playlist, path, run_event)
    player = music_player(playlist, run_event)

    listener.start()
    player.start()

    try:
        while True:
            time.sleep(.1)
    except KeyboardInterrupt:
        print "Keyboard Interrupt"
        run_event.clear()
        print "player closed"
        print "listener closed"
