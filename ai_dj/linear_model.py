import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn import set_config; set_config(display='diagram')
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import io
from tensorflow.python.lib.io import file_io
import pickle

def load_rated_mixes():
    f = io.BytesIO(
                file_io.read_file_to_string(
                    f'gs://ai_dj_batch627_data/data/rated_mixes/rated_mixes.csv',
                    binary_mode=True))
    df = np.load(f, allow_pickle=True)
    df = pd.DataFrame(df)
    df.columns=["mix_name", "bpm_difference", "camelot_distance", "z_cross_diff_original",
            "mean_ampl_diff_original", "min_freq_diff_original", "max_freq_diff_original",
            "range_freq_diff_original", "n_drums", "n_bass", "n_vocals", "n_other", 
            "mean_ampl_mix", "z_cross_mix", "rating"]
    # print(df.head(1))
    return df


def create_pipeline():
    num_columns = ["bpm_difference", "z_cross_diff_original", "mean_ampl_diff_original", 
               "min_freq_diff_original", "max_freq_diff_original", "range_freq_diff_original", 
               "mean_ampl_mix", "z_cross_mix"]
    cat_columns = ["camelot_distance"]

    num_transformer = Pipeline([
        ('scaler', StandardScaler())])

    cat_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer([
        ('num_transformer', num_transformer, num_columns),
        ('cat_transformer', cat_transformer, cat_columns)])
    
    final_pipe = Pipeline([
        ('preprocessing', preprocessor),
        ('linear_regression', LinearRegression())])

    return final_pipe

def update_model(df):
    df = df[df["rating"] != 0]
    X = df[["bpm_difference", "camelot_distance", "z_cross_diff_original",
            "mean_ampl_diff_original", "min_freq_diff_original", "max_freq_diff_original",
            "range_freq_diff_original", "n_drums", "n_bass", "n_vocals", "n_other", 
            "mean_ampl_mix", "z_cross_mix"]]
    y = df["rating"]
    final_pipe = create_pipeline()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    final_pipe_trained = final_pipe.fit(X_train,y_train)

    # Export pipeline as pickle file
    with open("pipeline.pkl", "wb") as file:
        pickle.dump(final_pipe_trained, file)
    return 