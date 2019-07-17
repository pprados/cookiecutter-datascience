import os
import pandas as pd

# Directory paths
dir_path = os.path.dirname(os.path.realpath(__file__))
output_path = os.path.join(dir_path, "../outputs")


def split_time_series(X, test_size=0.2):
    """
    Do a simple split at one time of the time series
    :param X: Features dataframe
    :param test_size: Proportion of observation in test
    :return: X_train, X_test
    """
    N = X.shape[0] # Number of observation
    i_split = int(N*test_size) # Position of the split
    return X.iloc[:i_split], X.iloc[i_split:]



if __name__ == "__main__":
    featured_df = pd.read_pickle(os.path.join(output_path, "prepared_data.p"))

    splits = split_time_series(featured_df)

    # Save all datasets in a pickle
    for name, data in zip(['train', 'test'], splits):
        pd.to_pickle(data, os.path.join(output_path, "prepared_" + name + ".p"))


