# Imports
import pandas as pd
import os
import numpy as np

# Directory paths
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, "../data")
output_path = os.path.join(dir_path, "../outputs")


def set_date_index(df):
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")


def get_dataset(name):
    """
    Return the dataset $name with its 'date' column as a DateTime index
    :param name: name for the file (name.csv)
    :return: the dataframe preprocesed
    """
    return pd.read_csv(os.path.join(data_path, "{}.csv").format(name))


def prepare_dataset(sensors, labels):
    """
    Pull the sensors and label datasets and merge them
    :return: one dataframe with sensors and labels
    """
    sensors = set_date_index(sensors)
    labels = set_date_index(labels)

    prepared_df = sensors.copy()
    prepared_df['state'] = labels['state']

    return prepared_df


if __name__ == "__main__":
    sensors, labels = get_dataset("sensors"), get_dataset("labels")
    prepared_df = prepare_dataset(sensors, labels)

    file_path = os.path.join(output_path, "prepared_data.p")
    prepared_df.to_pickle(file_path)

    print("A dataset of {} columns with {} has been prepared and stored at {}."
            .format(prepared_df.shape[1], prepared_df.shape[0], file_path))
