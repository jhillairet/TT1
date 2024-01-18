# -*- coding: utf-8 -*-
from dataclasses import dataclass
from pathlib import Path
import pandas as pd


@dataclass
class TT1TimeSeries:
    """
    TT-1 Generic Time Series.

    A Time Series is defined by:
    - a parameters dictionnary that contains
    informations concerning the data type, origin and unit.
    - a pandas DataFrame that contains the time series data

    Parameters
    ----------
    file : str, optional.
        Path to a TT-1 data text file (.txt). Default is ''.
    parameters : dict, optional
        Dictionnary of parameters. Default is empty dict.
    df : pd.DataFrame, optional
        Time Series data. Default is None

    Two way to instantiate the objetc:
        - provide a file
        - provide parameters and df

    """
    parameters: dict
    df: pd.DataFrame

    def __init__(self, file: str = "", parameters={}, df=None):
        if file == "":
            self.parameters = parameters
            self.df = df
        else:
            self.parameters, self.df = self._from_file(file)

    @staticmethod
    def _from_file(file: str):
        """
        Extract the data from a text file.

        Parameters
        ----------
        file : str
            Path to the text file.

        Returns
        -------
        parameters : dict
            Data Time Series Parameters.
        df : pandas.DataFrame
            Data Time Series.

        """
        parameters = {}

        file = Path(file)
        if file.exists():
            # extract data parameters
            with open(file, "r") as f:
                for line in f:
                    line = line.strip()

                    if not line or line.startswith("#"):
                        continue  # Skip empty lines and comments (lines starting with #)

                    if "=" in line:
                        key, value = map(str.strip, line.split("="))
                        parameters[key] = value

            # extract data values
            df = pd.read_csv(
                file,
                skiprows=8,
                sep="  ",
                names=["t", f'{parameters["SignalName"]} [{parameters["SignalUnit"]}]'],
                index_col="t",
                engine="python",
            )
        return parameters, df

    def __repr__(self):
        text = f'TT-1 #{self.parameters["ShotNo"]} {self.parameters["SignalName"]} data.'
        return text
