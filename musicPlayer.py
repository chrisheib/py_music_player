import wget
import os
from pygame import mixer
import sys
import threading
import time
from eyed3 import id3, load
from pynput.keyboard import Listener


GL_songname = './song.mp3'
GL_paused = False
next_song = False
GL_play_pause = False


def on_press(key):
    if str(key) == 'Key.media_play_pause':
        # play pause media key was pressed
        global GL_play_pause
        GL_play_pause = True

    if str(key) == 'Key.media_next':
        # next key was pressed
        global next_song
        next_song = True


class KeyboardPoller(threading.Thread):
    def run(self):
        global next_song
        while True:
            input("")
            next_song = True


def play(path):
    mixer.music.load(path)
    mixer.music.set_volume(0.2)
    mixer.music.play()
    global GL_paused
    GL_paused = False


def pause():
    mixer.music.pause()
    global GL_paused
    GL_paused = True


def resume():
    mixer.music.unpause()
    global GL_paused
    GL_paused = False


def stop():
    mixer.music.stop()
    mixer.music.unload()


def download():
    url = 'http://localhost:81/songs/random'

    if os.path.exists(GL_songname):
        os.remove(GL_songname)

    wget.download(url, GL_songname)
    print()


def print_songdata(path):
    tag = id3.tag.Tag()
    tag.parse(path)
    a = load(path)

    print("Now playing: % s - %s: %s (%s)" %
          (tag.title, tag.artist, tag.album, duration_from_seconds(a.info.time_secs)))


def duration_from_seconds(s):
    """Module to get the convert Seconds to a time like format."""
    s = s
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    _, h = divmod(h, 24)
    timelapsed = "{:02d}:{:02d}:{:02d}".format(int(h),
                                               int(m),
                                               int(s))
    return timelapsed


def toggle_play_pause():
    global GL_play_pause
    GL_play_pause = False
    if GL_paused:
        resume()
    else:
        pause()


def main():
    mixer.init()
    poller = KeyboardPoller()
    poller.start()

    listener_thread = Listener(on_press=on_press, on_release=None)
    listener_thread.start()

    while True:
        download()
        print_songdata(GL_songname)
        play(GL_songname)
        global next_song
        next_song = False
        print("Press enter for new song")

        while mixer.music.get_busy() and not next_song:
            if GL_play_pause:
                toggle_play_pause()
            time.sleep(0.1)

        stop()


if __name__ == "__main__":
    main()
