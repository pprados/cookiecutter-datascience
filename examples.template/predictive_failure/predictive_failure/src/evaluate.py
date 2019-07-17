import os
import pandas as pd
from sklearn.metrics import classification_report

if __name__ == "__main__":
    # Directory paths
    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.join(dir_path, "../outputs")

    # Pulling the model
    model = pd.read_pickle(os.path.join(output_path, "model.p"))

    # Pulling the test dataset
    data_test = pd.read_pickle(os.path.join(output_path, "featured_test.p"))
    X_test = data_test.drop("state", axis=1)
    y_test = data_test.state

    # Make the prediction
    y_pred = model.predict(X_test)

    metrics = pd.DataFrame.from_dict(classification_report(y_test, y_pred, output_dict=True)).T
    print(metrics)

    metrics.reset_index().to_csv(os.path.join(output_path, "metrics.csv"), index=False)

