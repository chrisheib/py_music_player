
import wget
import os
from pygame import mixer
import sys
import threading
import time

# this is to signal when the key_pressed flag has useful data,
# it will be "set" to indicate that the key_pressed flag has been set
# accordingly
data_ready = threading.Event()


class KeyboardPoller(threading.Thread):
    def run(self):
        global key_pressed
        while True:
            input("")
            key_pressed = True
            data_ready.set()


def play(path):
    mixer.music.load(path)
    mixer.music.set_volume(0.2)
    mixer.music.play()


def stop():
    mixer.music.stop()
    mixer.music.unload()


def download():
    #print('Beginning download...')
    url = 'http://localhost:81/songs/random'

    if os.path.exists('./song.mp3'):
        os.remove('./song.mp3')

    wget.download(url, './song.mp3')
    print()


def main():
    poller = KeyboardPoller()
    poller.start()
    mixer.init()

    while True:
        global key_pressed
        download()
        play('./song.mp3')
        key_pressed = False
        print("Press enter for new song")

        while not data_ready.isSet():
            time.sleep(0.01)

        while mixer.music.get_busy() and not key_pressed:
            time.sleep(0.1)

        stop()


if __name__ == "__main__":
    main()
