
import os
import pandas as pd
import numpy as np
from os.path import join
dir = "F:\CODEA\ReactionTimeApplication"
final_path = "F:\CODEA\ReactionTimeApplication\final_filtered.csv"
final_file = pd.read_csv(final_path)


save_frame = {
    "id": [],
    "gender": [],
    "age": [],

    "mean_RT_E1": [],
    "mean_RT_E2": [],

    "mean_RT_FP_E1": [],
    "mean_RT_FP_E2": [],
    "mean_RT_UP_E1": [],
    "mean_RT_UP_E2": [],

    "mean_RT_FPo_E1": [],
    "mean_RT_UPo_E1": [],
    "mean_RT_FPe_E1": [],
    "mean_RT_UPe_E1": [],
    

    "mean_RT_FPo_E2": [],
    "mean_RT_UPo_E2": [],
    "mean_RT_FPe_E2": [],
    "mean_RT_UPe_E2": [],
}


def get_new_par_dict():
    return{
    "gender": 'None',
    "age": 'None',

    "mean_RT_E1": [],
    "mean_RT_E2": [],

    "mean_RT_FP_E1": [],
    "mean_RT_FP_E2": [],
    "mean_RT_UP_E1": [],
    "mean_RT_UP_E2": [],

    "mean_RT_FPo_E1": [],
    "mean_RT_UPo_E1": [],
    "mean_RT_FPe_E1": [],
    "mean_RT_UPe_E1": [],
    

    "mean_RT_FPo_E2": [],
    "mean_RT_UPo_E2": [],
    "mean_RT_FPe_E2": [],
    "mean_RT_UPe_E2": [],
    }


participants_dict = {}


current_id = 0
for i in range(final_file.shape[0]):
    if current_id not in participants_dict:
        participants_dict[current_id] = get_new_par_dict

    current_id = str(final_file["id"][i])

    participants_dict[current_id]["gender"] = final_file["gender"][i]
    participants_dict[current_id]["age"] = final_file["age"][i]
    reaction_time = float(final_file["reaction_time"][i])

    if final_file["silent"][i] == 'True':
        if participants_dict["condition"][i] == "exp1":
            participants_dict[current_id]["mean_RT_E1"].append(reaction_time)

            participants_dict[current_id]["mean_RT_UP_E1"].append(reaction_time)

            if final_file["replaced"][i] == "öh":
                participants_dict[current_id]["mean_RT_UPo_E1"].append(reaction_time)
            else:
                participants_dict[current_id]["mean_RT_UPe_E1"].append(reaction_time)

        else:
            participants_dict[current_id]["mean_RT_E2"].append(reaction_time)

            participants_dict[current_id]["mean_RT_UP_E2"].append(reaction_time)

            if final_file["replaced"][i] == "öh":
                participants_dict[current_id]["mean_RT_UPo_E2"].append(reaction_time)
            else:
                participants_dict[current_id]["mean_RT_UPe_E2"].append(reaction_time)

    else:
        if final_file["condition"][i] == "exp1":
            participants_dict[current_id]["mean_RT_E1"].append(reaction_time)
            participants_dict[current_id]["mean_RT_FP_E1"].append(reaction_time)

            if final_file["pause_type"][i] == "öh":
                participants_dict[current_id]["mean_RT_FPo_E1"].append(reaction_time)
            else:
                participants_dict[current_id]["mean_RT_FPe_E1"].append(reaction_time)
        else:
            participants_dict[current_id]["mean_RT_E2"].append(reaction_time)
            participants_dict[current_id]["mean_RT_FP_E2"].append(reaction_time)

            if final_file["pause_type"][i] == "öh":
                participants_dict[current_id]["mean_RT_FPo_E2"].append(reaction_time)
            else:
                participants_dict[current_id]["mean_RT_FPe_E2"].append(reaction_time)

for key in participants_dict.keys():
    save_frame["id"].append(key)
    save_frame["gender"].append(participants_dict[key]["gender"])
    save_frame["age"].append(participants_dict[key]["age"])

    for key2 in save_frame.keys():
        if key2 == "id" or key2 == "gender" or key2 == "age": 
            continue
        else:
            save_frame[key2].append(sum(participants_dict[key][key2]) / len(participants_dict[key][key2]))

print(save_frame)








            





