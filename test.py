
import pandas as pd
from pydub import AudioSegment
import random
import simpleaudio as sa

from pydub.playback import _play_with_simpleaudio
import numpy as np
import time
import os
from pynput import keyboard
from os.path import isfile, join    

import multiprocessing

path_to_out = "/home/baserad/Documents/GitHub/ReactionTimeApplication/Data/out.xlsx"
bleep_effect = "/home/baserad/Documents/GitHub/ReactionTimeApplication/Bleep.mp3"

save_folder = "/home/baserad/Documents/GitHub/ReactionTimeApplication/Data/participants"

test_files = [
    AudioSegment.from_mp3(file="/home/baserad/Documents/GitHub/ReactionTimeApplication/test_files/hälsa.mp3"),
    AudioSegment.from_mp3(file="/home/baserad/Documents/GitHub/ReactionTimeApplication/test_files/dag.mp3"),
    AudioSegment.from_mp3(file="/home/baserad/Documents/GitHub/ReactionTimeApplication/test_files/åt_false.mp3"),
    AudioSegment.from_mp3(file="/home/baserad/Documents/GitHub/ReactionTimeApplication/test_files/marketplace.mp3"),
    AudioSegment.from_mp3(file="/home/baserad/Documents/GitHub/ReactionTimeApplication/test_files/djur.mp3"),
    AudioSegment.from_mp3(file="/home/baserad/Documents/GitHub/ReactionTimeApplication/test_files/teknologi.mp3"),
    AudioSegment.from_mp3(file="/home/baserad/Documents/GitHub/ReactionTimeApplication/test_files/djur1.mp3"),
    AudioSegment.from_mp3(file="/home/baserad/Documents/GitHub/ReactionTimeApplication/test_files/teknologi_false.mp3"),
]

test_words = [
    "hälsa",
    "dag",
    "åt",
    "marketplace",
    "djur",
    "teknologi",
    "djur",
    "teknologi"
]


print('\033[?25l', end="") 
os.system('clear')
bleep = AudioSegment.from_mp3(file=bleep_effect)[0:750]


if __name__ == "__main__":    
    def do_ting(audio, focus):
        os.system('clear')
        _play_with_simpleaudio(bleep)
        print(focus)
        time.sleep(1.5)
        seconds = audio.duration_seconds
        _play_with_simpleaudio(audio)
        time.sleep(seconds)

    command = input("demonstrate 1 or 2?: \n")

    print("experiment demonstration is about to start...")

    time.sleep(1)

    if command == "1":
        for i in range(4):
            do_ting(test_files[i], test_words[i])
    else:
        for i in range(4,8):
            do_ting(test_files[i], test_words[i])
        



    
