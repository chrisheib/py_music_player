
#from playsound import playsound
import wget
#import winsound
import os
# os.add_dll_directory(r'E:\Programmieren\Python\MusicPlayer\vlc-3.0.11')
#import vlc
#from mpyg321.mpyg321 import MPyg321Player
from pygame import mixer


#import multiprocessing


def play(path):
    # playsound(path)
    # winsound.PlaySound(path, winsound.SND_ASYNC)
    #p = multiprocessing.Process(target=playsound, args=(path,))
    # p.start()
    #p = vlc.MediaPlayer("file:///./song.mp3")
    # p.play
    # p.play_song(path)
    mixer.music.load(path)
    mixer.music.set_volume(0.2)
    mixer.music.play()
    # return p


def stop():
    # process.terminate()
    #winsound.PlaySound(None, winsound.SND_PURGE)
    mixer.music.stop()
    mixer.music.unload()


def download():
    print('Beginning download...')
    url = 'http://localhost:81/songs/random'

    if os.path.exists('./song.mp3'):
        os.remove('./song.mp3')

    wget.download(url, './song.mp3')
    print()


#p = MPyg321Player()
mixer.init()

while True:
    download()
    play('./song.mp3')
    input("press ENTER for new song")
    print()
    stop()
