import sys
from os import listdir
from os.path import isfile, join
from moviepy.editor import *
import time

save_path_audio = ""
save_path_video = ""
save_path_stimdata = ""
frame_rate = 30


def frames_to_seconds(frame_stamp):
    return int(frame_stamp) / frame_rate


def convert_to_audio(files):
    new_vid_paths = []
    new_audio_paths = []

    for f in files:
        name = f.split('/')[-1].split('.')[0]
        vid = VideoFileClip(f)
        audio_path = join(save_path_audio, name + ".mp3")
        video_path = join(save_path_video, name + ".mp4")

        vid.audio.write_audiofile(audio_path)
        vid.write_videofile(video_path)

        new_vid_paths.append(video_path)
        new_audio_paths.append(audio_path)

    return new_vid_paths, new_audio_paths

def add_to_dict(dict, id, key, value):
    if dict[id] == None:
        dict[id] = {"key": value}
    else:
        dict[id][key] = value



if __name__ == "__main__":
    print("Enter filepath to stimuli_data: ")
    stimuli_path = input()
    print("Enter path to timestamps: ")
    timepaths = input()


   # try:    
    file_ts = open(timepaths, "r")
    ts = file_ts.readlines()
    file_ts.close()
    clips_ts = ts.split("clip_start")

    clip_started_at = "00"
    start_frame = 0
    index = 0 
    info_dict = {}

    for line in ts:
        info = ts.split("||")
        marker, framenumber, comment = info[0], info[1], info[2]

        if marker == "clip_start":
            index += 1
            start_frame = framenumber
            add_to_dict(info_dict, index, "start", frames_to_seconds(framenumber))
        else:
            add_to_dict(info_dict, index, )


            
            start = datetime(timestamp,'%H:%M:%S:%f')

        
    for clip in clips_ts:
        annotations = clip.split("||")
        start_time = annotations[0]
        pause_type = annotations[1]
        pause_start =

    print(clips_ts)
        #onlyfiles = [f for f in listdir(stimuli_path) if isfile(join(stimuli_path, f))]
        #onlyfiles.sort(key = int(lambda x:x.split('/')[-1].split('.')[0][-1]))
      #  new_vid_paths, new_audio_paths = convert_to_audio(onlyfiles)

        
            
    #except:
     #   print("there was an error in one of the path names...")
     #   print("restart the program and try again.")
     #   input()






