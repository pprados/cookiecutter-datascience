# Imports
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import os

if __name__ == "__main__":
    # Directory paths
    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.join(dir_path, "../outputs")

    # Pulling the train dataset
    data_train = pd.read_pickle(os.path.join(output_path, "featured_train.p"))
    X_train = data_train.drop("state", axis=1)
    y_train = data_train.state

    print(X_train.head(10))
    # Fitting a simple model
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    pd.to_pickle(model, os.path.join(output_path, "model.p"))

    print("A model has been trained with {} features named :\n\t{}.".format(
        len(X_train.columns),
        ", ".join(X_train.columns)
    ))
