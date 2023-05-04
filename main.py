
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
print('\033[?25l', end="") 

bleep = AudioSegment.from_mp3(file=bleep_effect)[0:750]



def save_data(reaction_times, reacted_IDs, reacted_type, false_reacts, condition):
    save_frame = {
        "false_reacts": [false_reacts]
        }
    for i in range(len(reacted_IDs)):
        if "silent" in reacted_type[i]:
            save_frame[str(reacted_IDs[i]) + "s"] = [reaction_times[i]]
        else:
            save_frame[str(reacted_IDs[i])] = [reaction_times[i]]

    df = pd.DataFrame(save_frame)
    df.to_excel(join(save_folder, condition + "out.xlsx"))




if __name__ == "__main__":
    df = pd.read_excel(io=path_to_out)
    filler_exp_1 = []
    filler_exp_2 = []

    exp_1_ohs = {}
    exp_1_ehms = {}
    exp_2_ohs = {}
    exp_2_ehms = {}

    #loads all the data
    size = df.shape[0]
    for i in range(size):
        id = int(df.at[i, "id"])
        path = df.at[i, "out"]
        segment = AudioSegment.from_mp3(file = path)
        target = df.at[i, "target"]
        condition = df.at[i, "condition"]
    

        if df.at[i, "pause_type"] == "none":
            if condition == "exp1":
                filler_exp_1.append([segment, target])
            else:
                filler_exp_2.append([segment, target])
            continue
            
        pause_type = df.at[i, "pause_type"]

        if pause_type == "silent":
            replaced_type = df.at[i, "replaced"]

            if replaced_type == "öh":
                if condition == "exp1":
                    if not id in exp_1_ohs: 
                        exp_1_ohs[id] = {}

                    exp_1_ohs[id]["silent"] = [segment, target]
                elif condition == "exp2":
                    if not id in exp_2_ohs:
                        exp_2_ohs[id] = {}

                    exp_2_ohs[id]["silent"] = [segment, target]

            elif replaced_type == "ehm":
                if condition == "exp1":
                    if not id in exp_1_ehms:
                        exp_1_ehms[id] = {}
                    exp_1_ehms[id]["silent"] = [segment, target]

                elif condition == "exp2":
                    if not id in exp_2_ehms:
                        exp_2_ehms[id] = {}
                    exp_2_ehms[id]["silent"] = [segment, target]

        else:
            if pause_type == "öh":
                if condition == "exp1":
                    if not id in exp_1_ohs: 
                        exp_1_ohs[id] = {}

                    exp_1_ohs[id]["filled"] = [segment, target]

                elif condition == "exp2":
                    if not id in exp_2_ohs:
                        exp_2_ohs[id] = {}

                    exp_2_ohs[id]["filled"] = [segment, target]
            elif pause_type == "ehm":
                  if condition == "exp1":

                    if not id in exp_1_ehms:
                        exp_1_ehms[id] = {}
                    exp_1_ehms[id]["filled"] = [segment, target]

                  elif condition == "exp2":
                    if not id in exp_2_ehms:

                        exp_2_ehms[id] = {}
                    exp_2_ehms[id]["filled"] = [segment, target]

    # randomizes all the data
    random_silence_numbers = [[], [], [], []]
    random_filled_numbers = [[], [], [], [],]


    for i in range(7):
        a = random.randint(0, 14)
        b = random.randint(0, 14)
        c = random.randint(0, 14)
        d = random.randint(0, 14)
        n_ = [a,b,c,d]
        for i in range(len(n_)):
            while n_[i] in random_silence_numbers[i]:
                n_[i] = random.randint(0, 14)
            random_silence_numbers[i].append(n_[i])
        
    for i in range(len(random_silence_numbers)):
        random_exclude = random.randint(0, 14)
        while random_exclude in random_silence_numbers[i]:
            random_exclude = random.randint(0, 14)

        random_filled_numbers[i] = np.arange(0, 15).tolist()
        random_filled_numbers[i].remove(random_exclude)

        for j in range(len(random_silence_numbers[i])):
            random_filled_numbers[i].remove(random_silence_numbers[i][j])
    
    def experiment_1():
        print()
        print("experiment 1 is about to start...")
        time.sleep(0.5)

        all_lines = []
        for filler in filler_exp_1:
            all_lines.append(["filler"] + filler)

        i = 0
        for key, value in exp_1_ohs.items():
            if i in random_silence_numbers[0]:
                all_lines.append([key, "silent_oh"] + value["silent"])
            elif i in random_filled_numbers[0]:
                all_lines.append([key, "filled_oh"] + value["filled"])
            i += 1
    
        i = 0
        for key, value in exp_1_ehms.items():
            if i in random_silence_numbers[1]:
                all_lines.append([key, "silent_ehm"] + value["silent"])
            elif i in random_filled_numbers[1]:
                all_lines.append([key, "filled_ehm"] + value["filled"])
            i += 1 
    
        random.shuffle(all_lines)

        reaction_times = []
        false_reacts_filler = 0
        reacted_IDs = []
        reacted_type = []

        for line in all_lines:

            os.system('clear')
            print()
            _play_with_simpleaudio(bleep)
            print(line[-1])
            time.sleep(1.5)
            os.system('clear')
            seconds = line[-2].duration_seconds
            _play_with_simpleaudio(line[-2])
            start_time = time.perf_counter()
            has_reacted = False
            reaction_time = 'none'
      
            while time.perf_counter() - start_time < seconds:
                remaining_seconds = seconds - (time.perf_counter() - start_time)
                if remaining_seconds > 0.001:
                    with keyboard.Events() as events:
                        event = events.get(remaining_seconds)
                        if not has_reacted:
                            if event != None:
                                if event.key == keyboard.Key.space:       
                                    has_reacted = True
                                    reaction_time = time.perf_counter() - start_time


            
            if "filler" in str(line[0]):
                if has_reacted:
                    false_reacts_filler += 1
            else:
                reaction_times.append(reaction_time)

                reacted_IDs.append(line[0])
                reacted_type.append(line[1])
    
        save_data(reaction_times, reacted_IDs, reacted_type, false_reacts_filler, "exp1")
        print("experiment 1 completed.")
    
    def experiment_2():
        print()
        print("experiment 2 is about to start...")
        time.sleep(0.5)

        all_lines = []
        for filler in filler_exp_2:
            all_lines.append(["filler"] + filler)

        i = 0
        for key, value in exp_2_ohs.items():
            if i in random_silence_numbers[2]:
                all_lines.append([key, "silent_oh"] + value["silent"])
            elif i in random_filled_numbers[2]:
                all_lines.append([key, "filled_oh"] + value["filled"])
            i += 1
    
        i = 0
        for key, value in exp_2_ehms.items():
            if i in random_silence_numbers[3]:
                all_lines.append([key, "silent_ehm"] + value["silent"])
            elif i in random_filled_numbers[3]:
                all_lines.append([key, "filled_ehm"] + value["filled"])
            i += 1 
    
        random.shuffle(all_lines)

        reaction_times = []
        false_reacts_filler = 0
        reacted_IDs = []
        reacted_type = []

        for line in all_lines:

            os.system('clear')
            print()
            _play_with_simpleaudio(bleep)
            print(line[-1])
            time.sleep(1.5)
            os.system('clear')
            seconds = line[-2].duration_seconds
            _play_with_simpleaudio(line[-2])
            start_time = time.perf_counter()
            has_reacted = False
            reaction_time = 'none'
      
            while time.perf_counter() - start_time < seconds:
                remaining_seconds = seconds - (time.perf_counter() - start_time)
                if remaining_seconds > 0.001:
                    with keyboard.Events() as events:
                        event = events.get(remaining_seconds)
                        if not has_reacted:
                            if event != None:
                                if event.key == keyboard.Key.space:       
                                    has_reacted = True
                                    reaction_time = time.perf_counter() - start_time


            
            if "filler" in str(line[0]):
                if has_reacted:
                    false_reacts_filler += 1
            else:
                reaction_times.append(reaction_time)

                reacted_IDs.append(line[0])
                reacted_type.append(line[1])
    
        save_data(reaction_times, reacted_IDs, reacted_type, false_reacts_filler, "exp2")
        print("experiment 2 completed.")

    command = input("Which experiment would you like to conduct first? (1 or 2): \n")

    if command == "1":
        experiment_1()
        input("press enter to start experiment 2")
        experiment_2()
        input("TACK FÖR ATT DU DELTOG I MIN STUDIE! :))) ")
    else:
        experiment_2()
        input("press enter to start experiment 1")
        experiment_1()
        input("TACK FÖR ATT DU DELTOG I MIN STUDIE! :))) ")
