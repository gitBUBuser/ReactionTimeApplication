
import os
import pandas as pd
import numpy as np
from os.path import join
participants_path = "/home/baserad/Documents/GitHub/ReactionTimeApplication/Data/participants"
out_path = "/home/baserad/Documents/GitHub/ReactionTimeApplication/Data/out.xlsx"

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

# först -- jag vill få reaktionstider per stimuli
out_file = pd.read_excel(out_path, engine='openpyxl')

def save_frame(stimuli):
    frame = {}
    for stim in stimuli:
        frame[stim] = []
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

for participant_folder in os.listdir(participants_path):
    p_path = join(participants_path, participant_folder)
    
    for excel_path in os.listdir(p_path):
        r_excel = pd.read_excel(join(p_path, excel_path), engine='openpyxl')

        # gets a list  of the stimuli the participant reacted to in the experimental condition
        stimulis = r_excel.axes[1][2:]
        for stimuli in stimulis:
            print()
            time_pressed = r_excel.loc[:,stimuli][0]
            if time_pressed != 'none':
                time_of_stimuli_start = float(access_stimuli_start(out_file, stimuli))
                reaction_time = float(time_pressed) - time_of_stimuli_start
                print(stimuli)
                print("stimuli starts at: ",time_of_stimuli_start)
                print("reaction is at: ", time_pressed)
                print("reaction time is: ", reaction_time)
                save_f[str(stimuli)].append(reaction_time)
            else:
                print(stimuli)
                print('missed')
                save_f[str(stimuli)].append('missed')

                
df = pd.DataFrame(save_f)
print(df)
            
            
                


        
    