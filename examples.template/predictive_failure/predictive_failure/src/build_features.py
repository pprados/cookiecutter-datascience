import os
import pandas as pd
import numpy as np

# Directory paths
dir_path = os.path.dirname(os.path.realpath(__file__))
output_path = os.path.join(dir_path, "../outputs")


def split_day(x):
    res = pd.Series(0, index=x.index)   # Init and default to zero
    res.loc[((7 <= x.dt.hour) & (x.dt.hour <= 11))] = 1
    res.loc[((11 < x.dt.hour) & (x.dt.hour <= 14))] = 2
    res.loc[((14 < x.dt.hour) & (x.dt.hour <= 19))] = 3
    res = res.astype(np.int)
    return res


def days_running(states):
    res = []
    n_current = 0
    for idx, state in states.iteritems():
        if (state == "ok"):
            n_current += 1
        if (state == "failure" or state == "restart"):
            n_current = 0

        res.append(n_current)
    return pd.Series(res, index=states.index)


def build_features(prepared_df):
    features = prepared_df.drop("state", axis=1)

    # Rolling features
    for rolling_period in [6]:
        rolling = features.rolling(rolling_period, win_type='triang')
        rolling_mean = rolling.mean().add_prefix('mean_{}'.format(rolling_period))
        features = features.join(rolling_mean)

    # Build features
    dates = pd.Series(features.index, index=features.index)
    features['part_of_day'] = split_day(dates)
    #features["days_running"] = days_running(prepared_df.state)

    # Building final dataset
    features = features.join(prepared_df.state)
    features.dropna(inplace=True)
    return features


if __name__ == "__main__":

    for name in ["train", "test"]:
        prepared_df = pd.read_pickle(os.path.join(output_path, "prepared_" + name + ".p"))
        features = build_features(prepared_df)

        file_path = os.path.join(output_path, "featured_" + name + ".p")
        features.to_pickle(file_path)

        print("Features with {} columns with {} observations has been stored at {}."
              .format(prepared_df.shape[1] - 1, prepared_df.shape[0], file_path))
