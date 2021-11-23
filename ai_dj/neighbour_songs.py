import pandas as pd

def create_camelot_wheel():
    camelot_wheel = pd.DataFrame()
    camelot_wheel["cw_number"] = ""
    camelot_wheel["key"] = ""
    camelot_wheel["neighbor_top"] = ""
    camelot_wheel["neighbor_left"] = ""
    camelot_wheel["neighbor_right"] = ""
    
    A1_k="g# min"
    A2_k='d# min'
    A3_k='a# min'
    A4_k='f min'
    A5_k='c min'
    A6_k='g min'
    A7_k='d min'
    A8_k='a min'
    A9_k='e min'
    A10_k='b min'
    A11_k='f# min'
    A12_k='c# min'
    B1_k='B Maj'
    B2_k='F# Maj'
    B3_k='C# Maj'
    B4_k='G# Maj'
    B5_k='D# Maj'
    B6_k='A# Maj'
    B7_k='F Maj'
    B8_k='C Maj'
    B9_k='G Maj'
    B10_k='D Maj'
    B11_k='A Maj'
    B12_k='E Maj'
    
    A1_dict = {"cw_number": "1A", "key":A1_k, "neighbor_top":B1_k, "neighbor_left":A12_k, "neighbor_right":A2_k}
    A2_dict = {"cw_number": "2A", "key":A2_k, "neighbor_top":B2_k, "neighbor_left":A1_k, "neighbor_right":A3_k}
    A3_dict = {"cw_number": "3A", "key":A3_k, "neighbor_top":B3_k, "neighbor_left":A2_k, "neighbor_right":A4_k}
    A4_dict = {"cw_number": "4A", "key":A4_k, "neighbor_top":B4_k, "neighbor_left":A3_k, "neighbor_right":A5_k}
    A5_dict = {"cw_number": "5A", "key":A5_k, "neighbor_top":B5_k, "neighbor_left":A4_k, "neighbor_right":A6_k}
    A6_dict = {"cw_number": "6A", "key":A6_k, "neighbor_top":B6_k, "neighbor_left":A5_k, "neighbor_right":A7_k}
    A7_dict = {"cw_number": "7A", "key":A7_k, "neighbor_top":B7_k, "neighbor_left":A6_k, "neighbor_right":A8_k}
    A8_dict = {"cw_number": "8A", "key":A8_k, "neighbor_top":B8_k, "neighbor_left":A7_k, "neighbor_right":A9_k}
    A9_dict = {"cw_number": "9A", "key":A9_k, "neighbor_top":B9_k, "neighbor_left":A8_k, "neighbor_right":A10_k}
    A10_dict = {"cw_number": "10A", "key":A10_k, "neighbor_top":B10_k, "neighbor_left":A9_k, "neighbor_right":A11_k}
    A11_dict = {"cw_number": "11A", "key":A11_k, "neighbor_top":B11_k, "neighbor_left":A10_k, "neighbor_right":A12_k}
    A12_dict = {"cw_number": "12A", "key":A12_k, "neighbor_top":B12_k, "neighbor_left":A11_k, "neighbor_right":A1_k}

    B1_dict = {"cw_number": "1B", "key":B1_k, "neighbor_top":A1_k, "neighbor_left":B12_k, "neighbor_right":B2_k}
    B2_dict = {"cw_number": "2B", "key":B2_k, "neighbor_top":A2_k, "neighbor_left":B1_k, "neighbor_right":B3_k}
    B3_dict = {"cw_number": "3B", "key":B3_k, "neighbor_top":A3_k, "neighbor_left":B2_k, "neighbor_right":B4_k}
    B4_dict = {"cw_number": "4B", "key":B4_k, "neighbor_top":A4_k, "neighbor_left":B3_k, "neighbor_right":B5_k}
    B5_dict = {"cw_number": "5B", "key":B5_k, "neighbor_top":A5_k, "neighbor_left":B4_k, "neighbor_right":B6_k}
    B6_dict = {"cw_number": "6B", "key":B6_k, "neighbor_top":A6_k, "neighbor_left":B5_k, "neighbor_right":B7_k}
    B7_dict = {"cw_number": "7B", "key":B7_k, "neighbor_top":A7_k, "neighbor_left":B6_k, "neighbor_right":B8_k}
    B8_dict = {"cw_number": "8B", "key":B8_k, "neighbor_top":A8_k, "neighbor_left":B7_k, "neighbor_right":B9_k}
    B9_dict = {"cw_number": "9B", "key":B9_k, "neighbor_top":A9_k, "neighbor_left":B8_k, "neighbor_right":B10_k}
    B10_dict = {"cw_number": "10B", "key":B10_k, "neighbor_top":A10_k, "neighbor_left":B9_k, "neighbor_right":B11_k}
    B11_dict = {"cw_number": "11B", "key":B11_k, "neighbor_top":A11_k, "neighbor_left":B10_k, "neighbor_right":B12_k}
    B12_dict = {"cw_number": "12B", "key":B12_k, "neighbor_top":A12_k, "neighbor_left":B11_k, "neighbor_right":B1_k}

    dicts = [A1_dict, A2_dict, A3_dict, A4_dict, A5_dict, A6_dict, A7_dict, A8_dict, A9_dict, A10_dict, A11_dict, A12_dict, 
            B1_dict, B2_dict, B3_dict, B4_dict, B5_dict, B6_dict, B7_dict, B8_dict, B9_dict, B10_dict, B11_dict, B12_dict]
    
    camelot_wheel = camelot_wheel.append(dicts, ignore_index=True)
    return camelot_wheel

# def get_neighbor_keys(key):
#     camelot_wheel = create_camelot_wheel()
#     cl_key = camelot_wheel[camelot_wheel["key"] == key]
#     neighbor_top = cl_key["neighbor_top"].values[0]
#     neighbor_left = cl_key["neighbor_left"].values[0]
#     neighbor_right = cl_key["neighbor_right"].values[0]
#     neighbors = [key, neighbor_top, neighbor_left, neighbor_right]
#     return neighbors

# def filter_bpm_keys(output_file, bpm, key):
#     gcp_storage.get_audio_features_csv()
#     audio_df = pd.read_csv(f'{params.DATA_FOLDER}/{params.AUDIO_FEATURES_FILE}', index_col=0)
#     audio_df = audio_df.drop(columns=["beat_frames", "beat_times"])
#     audio_df = audio_df[audio_df["output_file"] != output_file]
#     audio_df["BPM"] = audio_df["BPM"].round()
#     bpms = [round(bpm), round(bpm/2)]
#     print(bpms)
#     bpm_df = audio_df[audio_df["BPM"].isin(bpms)]
#     same_key_df = bpm_df[bpm_df["key"] == key]
#     if len(same_key_df) > 1:
#         return same_key_df
#     else:
#         neigborgs = get_neighbor_keys(key)
#         print(neigborgs)
#         neigborgs_key_df = bpm_df[bpm_df["key"].isin(neigborgs)]
#         print(neigborgs_key_df)
#         return neigborgs_key_df

# def select_songs(neighbors_songs):
#     two_songs = neighbors_songs.sample(2)
#     return two_songs

## Test
#neighbors_songs = filter_bpm_keys(139.6748310810811, "G# Maj")
#print(neighbors_songs["title"], neighbors_songs["BPM"], neighbors_songs["key"])
#neighbor_keys = get_neighbor_keys("a min")
#print(neighbor_keys)
## Test
