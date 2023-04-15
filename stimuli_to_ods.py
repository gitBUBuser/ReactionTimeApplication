import sys
import os
from os import listdir
from os.path import isfile, join
import time
import pandas as pd
from pydub import AudioSegment
from pydub.playback import play
import copy


dir = "/home/baserad/Documents/GitHub/ReactionTimeApplication/"

save_path_stimdata = os.path.join(dir, "Data/")
path_to_guides = os.path.join(dir,"Data/Labels_ebben.txt")
path_to_audio = os.path.join(dir, "Data/data_ebben.mp3")

exp1_filled_stimuli_output = os.path.join(dir, "Data/Stimuli/Data/Experiment1/real/filled")
exp1_silent_stimuli_output = os.path.join(dir,"Data/Stimuli/Data/Experiment1/real/quiet")
exp2_filled_stimuli_output = os.path.join(dir, "Data/Stimuli/Data/Experiment2/real/filled")
exp2_silent_stimuli_output = os.path.join(dir,"Data/Stimuli/Data/Experiment2/real/silent")
exp1_filler_output = os.path.join(dir, "Data/Stimuli/Data/Experiment1/filler")
exp2_filler_output = os.path.join(dir, "Data/Stimuli/Data/Experiment2/filler")

def cast(value):
    return float(value)

def get_frames(file):
    with open(file) as f:
        labels = f.read()
        labeled_tracks = {}
        track_index_int  = 0

        tracks = labels.split("*")

        for track in tracks:
            lines = track.split("\n")
            for line in lines:
                
                annotations  = line.split()
                
                if(len(annotations) < 3):
                    continue

                start, end, annotation = annotations[0], annotations[1], annotations[2]
                s_annotation = annotation.split('_')

                if s_annotation[0] == "track":
                    track_index_int += 1
                    track_index = str(track_index_int)
                    labeled_tracks[track_index] = {}
                    labeled_tracks[track_index]["condition"] = s_annotation[-1]
                    labeled_tracks[track_index]["start"], labeled_tracks[track_index]["end"] = cast(start), cast(end)
                    labeled_tracks[track_index]["duration"] = cast(end) - cast(start)
                    if s_annotation[1] == "filler":
                        labeled_tracks[track_index]["filler"] = "True"
                        labeled_tracks[track_index]["target"] = s_annotation[2]
                        labeled_tracks[track_index]["stimuli_target"] = annotation.split("_")[-1]
                        labeled_tracks[track_index]["stimuli_start"], labeled_tracks[track_index]["stimuli_end"] = 0, 0
                        labeled_tracks[track_index]["stimuli_duration"] = 0
                        labeled_tracks[track_index]["pause_type"] = "none"
                        labeled_tracks[track_index]["pause_start"], labeled_tracks[track_index]["pause_end"] = 0, 0
                        labeled_tracks[track_index]["pause_duration"] = 0

                    else:
                        labeled_tracks[track_index]["filler"] = "False"
        
                elif "pause" in annotation:
                    labeled_tracks[track_index]["pause_type"] = annotation.split("_")[-1]
                    labeled_tracks[track_index]["pause_start"], labeled_tracks[track_index]["pause_end"] = cast(start), cast(end)
                    labeled_tracks[track_index]["pause_duration"] = cast(end) - cast(start)
                elif "stimuli" in annotation:
                    labeled_tracks[track_index]["target"] = annotation.split("_")[-1]
                    labeled_tracks[track_index]["stimuli_start"], labeled_tracks[track_index]["stimuli_end"] = cast(start), cast(end)
                    labeled_tracks[track_index]["stimuli_duration"] = cast(end) - cast(start)
        
        for key in labeled_tracks.keys():
            start = labeled_tracks[key]["start"]
            labeled_tracks[key]["relative_pause_onset"] = labeled_tracks[key]["pause_start"] - start
            labeled_tracks[key]["relative_pause_end"] = labeled_tracks[key]["pause_end"] - start
            labeled_tracks[key]["relative_stimuli_onset"] = labeled_tracks[key]["stimuli_start"] - start
            labeled_tracks[key]["relative_stimuli_end"] = labeled_tracks[key]["stimuli_end"] - start

    return labeled_tracks

def add_segments(audio, tracks):
    for key in tracks.keys():
        ms_start = tracks[key]["start"] * 1000
        ms_end = tracks[key]["end"] * 1000
        tracks[key]["audio"] = audio[ms_start:ms_end]

def generate_quiet_pauses(audio, tracks):
    silent_tapes = {}
    for key in tracks.keys():
        if tracks[key]["filler"] == "False":
            ms_start = tracks[key]["start"] * 1000
            ms_end = tracks[key]["end"] * 1000
            ms_pause_start = tracks[key]["pause_start"] * 1000
            ms_pause_end = tracks[key]["pause_end"] * 1000
            ms_pause_duration = tracks[key]["pause_duration"] * 1000

            new_key = str(key) + "s"
        
            silent_pause_track = tracks[key].copy()
            silent_pause_track["pause_type"] = "silent"

            silent_pause = AudioSegment.silent(duration=ms_pause_duration)
            silent_pause_track["audio"] = audio[ms_start:ms_pause_start] + silent_pause + audio[ms_pause_end:ms_end]
            silent_tapes[new_key] = silent_pause_track

    for key_2, value in silent_tapes.items():
        tracks[key_2] = value



        
    
        



def add_outputs(tracks):
    for key in tracks.keys():
        if tracks[key]["filler"] == "True":
            if tracks[key]["condition"] == "exp1":
                tracks[key]["out"] = join(exp1_filler_output, f"track_{key}.mp3")
            else:
                tracks[key]["out"] = join(exp2_filler_output, f"track_{key}.mp3")
        else:
            if tracks[key]["condition"] == "exp1":
                if "s" in key:
                    tracks[key]["out"] = join(exp1_silent_stimuli_output, f"track_{key}.mp3")
                else:
                    tracks[key]["out"] = join(exp1_filled_stimuli_output, f"track_{key}.mp3")
            else:
                if "s" in key:
                    tracks[key]["out"] = join(exp2_silent_stimuli_output, f"track_{key}.mp3")
                else:
                    tracks[key]["out"] = join(exp2_filled_stimuli_output, f"track_{key}.mp3")

def save_data(tracks):
    save_frame = {
        "out": [],
        "condition": [],
        "duration": [],
        "relative_pause_onset": [],
        "relative_pause_end": [],
        "pause_duration": [],
        "pause_type": [],
        "relative_stimuli_onset": [],
        "relative_stimuli_end": [],
        "stimuli_duration": [],
        "target": []
    }

    for key in tracks.keys():
        for key2 in save_frame.keys():
            save_frame[key2].append(tracks[key][key2])

        tracks[key]["audio"].export(out_f = tracks[key]["out"], format = "mp3")
    df = pd.DataFrame(save_frame)
    df.to_excel(join(save_path_stimdata, "out.xlsx"))
    

    

print(path_to_audio)
print(path_to_guides)
print(dir)
frames = get_frames(path_to_guides)
audio = AudioSegment.from_mp3(path_to_audio)
add_segments(audio, frames)
generate_quiet_pauses(audio, frames)
add_outputs(frames)
save_data(frames)