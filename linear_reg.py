import numpy as np
import pandas as pd



class LinearRegressionModel:
    """
    A multi-feature linear regression model that can be fit and used for prediction
    """

    def __init__(self):
        """
        Initializes a linear regression model
        """
        self.weights = None


    def fit(self, x: pd.DataFrame, y):
        """
        Fit/train this linear regression model on the provided inputs and matching outputs
        :param x: Dataframe containing the features
        :param y: Series containing all output values
        """
        # Add column of ones in order to handle y-intercept
        # Get numpy array
        x_mat = x.to_numpy()

        # Apply matrix equation in order to get the weights
        self.weights = np.matmul(np.matmul(np.linalg.inv(np.matmul(x_mat.T, x_mat)), x_mat.T), y.to_numpy())


    def predict(self, x: pd.DataFrame) -> pd.Series:
        """
        Predicts the output variables given all input features
        :param x: Dataframe containing features
        :return: a Series containing the outputs
        """
        # Add column of ones in order to handle y-intercept
        x_mat = x.to_numpy()
        # Multiply weights by x matrix
        result = np.matmul(x_mat, self.weights)
        return pd.Series(result)


    def get_weights(self, column_names):
        """
        Adds each weight to a dictionary with their respective column name
        :param column_names: list of all the column names
        :return: a dictionary mapping column name to weight
        """
        weight_dict = dict()
        for i in range(len(column_names)):
            weight_dict[column_names[i]] = self.weights[i]
        return weight_dict