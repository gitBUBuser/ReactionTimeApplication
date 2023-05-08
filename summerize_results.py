
import os
import pandas as pd
import numpy as np
from os.path import join
dir = "/home/baserad/Documents/GitHub/ReactionTimeApplication/"
participants_path = "/home/baserad/Documents/GitHub/ReactionTimeApplication/Data/participants"
out_path = "/home/baserad/Documents/GitHub/ReactionTimeApplication/Data/out.xlsx"
save_path_stimdata = join(dir, "Data/")

def access_stimuli_start(df, attribute):
    if 's' in attribute:
        id = attribute.replace('s', '')
        relevant_indeces = np.arange(120, df.shape[0])
        for i in relevant_indeces:
            stimuli_id = df['id'][i]
            if float(stimuli_id) == float(id):
                return df['relative_stimuli_onset'][i]
    else:
        id = attribute
        relevant_indeces = np.arange(0, 120)
        for i in relevant_indeces:
            stimuli_id = df['id'][i]
            if float(stimuli_id) == float(id):
                return df['relative_stimuli_onset'][i]

def access_stimuli_property(df, attribute_id, attribute):
    if 's' in attribute_id:
        id = attribute_id.replace('s', '')
        relevant_indeces = np.arange(120, df.shape[0])
        for i in relevant_indeces:
            stimuli_id = df['id'][i]
            if float(stimuli_id) == float(id):
                return df[attribute][i]
    else:
        id = attribute_id
        relevant_indeces = np.arange(0, 120)
        for i in relevant_indeces:
            stimuli_id = df['id'][i]
            if float(stimuli_id) == float(id):
                return df[attribute][i]


# först -- jag vill få reaktionstider per stimuli
out_file = pd.read_excel(out_path, engine='openpyxl')


def save_frame(stimuli):
    frame = {
        "participant_id": [],
        "age": [],
        "gender": [],
        "reaction_time": [],
        "stimuli_id": [],
        "condition": [],
        "pause_length": [],
        "pause_onset": [],
        "pause_type": [],
        "stimuli_length": [],
        "stimuli_onset": [],
        "replaced": [],
        "target": [],
        "handedness": []
    }
    return frame
    

print(out_file.shape[0])
stimulus = []
for i in range(out_file.shape[0]):
    print(out_file['filler'][i])
    if str(out_file['filler'][i]) == "False":
        if str(out_file["pause_type"][i]) == "silent":
            stimulus.append(str(out_file["id"][i]) + "s")
        else:
            stimulus.append(str(out_file["id"][i]))
    else:
        continue


save_f = save_frame(stimulus)
id = 0
for participant_folder in os.listdir(participants_path):
    id += 1
    p_path = join(participants_path, participant_folder)
    p_info = pd.read_excel(join(p_path, "p_data.xlsx"), engine='openpyxl')
    p_id = id
    gender = p_info["Kön"][0]
    age = p_info["Ålder"][0]
    handedness = p_info["Handedness"][0]
    for excel_path in os.listdir(p_path):
        if "p_data" in excel_path:
            continue

        r_excel = pd.read_excel(join(p_path, excel_path), engine='openpyxl')

        # gets a list  of the stimuli the participant reacted to in the experimental condition
        stimulis = r_excel.axes[1][2:]
        for stimuli in stimulis:
            print()
            time_pressed = r_excel.loc[:,stimuli][0]
            if time_pressed != 'none':
                time_of_stimuli_start =  float(access_stimuli_property(out_file, stimuli, "relative_stimuli_onset"))
                reaction_time = float(time_pressed) - time_of_stimuli_start
            #    print(stimuli)
            #    print("stimuli starts at: ",time_of_stimuli_start)
            #    print("reaction is at: ", time_pressed)
            #    print("reaction time is: ", reaction_time)
                save_f["age"].append(age)
                save_f["participant_id"].append(p_id)
                save_f["gender"].append(gender)
                save_f["stimuli_id"].append(stimuli)
                save_f["reaction_time"].append(reaction_time)
                save_f["condition"].append(access_stimuli_property(out_file, stimuli, "condition"))
                save_f["replaced"].append(access_stimuli_property(out_file, stimuli, "replaced"))
                save_f["pause_type"].append(access_stimuli_property(out_file, stimuli, "pause_type"))
                save_f["pause_onset"].append(access_stimuli_property(out_file, stimuli, "relative_pause_onset"))
                save_f["stimuli_onset"].append(time_of_stimuli_start)
                save_f["pause_length"].append(access_stimuli_property(out_file, stimuli, "pause_duration"))
                save_f["stimuli_length"].append(access_stimuli_property(out_file, stimuli, "stimuli_duration"))
                save_f["target"].append(access_stimuli_property(out_file, stimuli, "target"))
                save_f["handedness"].append(handedness)

            else:
                save_f["age"].append(age)
                save_f["participant_id"].append(p_id)
                save_f["gender"].append(gender)
                save_f["stimuli_id"].append(stimuli)
                save_f["reaction_time"].append("missed")
                save_f["pause_type"].append(access_stimuli_property(out_file, stimuli, "pause_type"))
                save_f["condition"].append(access_stimuli_property(out_file, stimuli, "condition"))
                save_f["replaced"].append(access_stimuli_property(out_file, stimuli, "replaced"))
                save_f["pause_onset"].append(access_stimuli_property(out_file, stimuli, "relative_pause_onset"))
                save_f["stimuli_onset"].append(time_of_stimuli_start)
                save_f["pause_length"].append(access_stimuli_property(out_file, stimuli, "pause_duration"))
                save_f["stimuli_length"].append(access_stimuli_property(out_file, stimuli, "stimuli_duration"))
                save_f["target"].append(access_stimuli_property(out_file, stimuli, "target"))
                save_f["handedness"].append(handedness)

print(save_f)
                
df = pd.DataFrame(save_f)
df.to_excel(join(save_path_stimdata, "final.xlsx"))
            
            
                


        
    