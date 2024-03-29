import pandas as pd
import numpy as np
from pathlib import Path

from .timeseries import TT1TimeSeries


class TT1Pulse:
    """
    TT-1 Pulse data.

    Parameters
    ----------
    pulse : int
        Pulse number.
    read_all : bool, optional
        If True, read all the time series file located in the directory.
        If False, read only the time series defined in the data_params dict.
        The default is False.

    Raises
    ------
    FileExistsError
        If the pulse data are not found.


    """

    R = 0.6  # major radius in meter
    a = 0.25  # minor radius in meter
    DATA_PATH = "data"
    data_params = {
        "IT2": "Toroidal Current",
        "IP1": "Plasma Current from left-side chamber",
        "IP2": "Plasma Current from right-side chamber",
        "GP": "Gas Puffing",
        "HCN1": "HCN Interf HFS",
        "HCN2": "HCN Interf Center",
    }

    def __init__(self, pulse: int, read_all: bool = False):
        self.p = Path(self.DATA_PATH + "/" + str(pulse)).absolute()
        print(self.p)

        if not self.p.exists():
            raise FileExistsError("The specified pulse data do not exist.")

        self.pulse = pulse
        self._read_data(self.p, read_all)

    def _read_data(self, path, read_all: bool = False):
        """
        Read time series for a TT-1 pulse data directory.

        Parameters
        ----------
        path : pathlib.Path
            Path to a directory.
        read_all : bool, optional
            If True, read all the time series file located in the directory.
            If False, read only the time series defined in the data_params dict.

        Returns
        -------
        None.

        """
        # extract all the data from this pulse
        self.data = {}

        if read_all:
            # read all available time series (longer)
            for timeseries_file in path.glob("*.txt"):
                param_name = timeseries_file.name.split(".")[0]
                self.data[param_name] = TT1TimeSeries(file=timeseries_file)
        else:
            # read only a selection of time series, defined in self.data_params
            for param in self.data_params.keys():
                file = path / f"{param}.txt"

                if file.exists():
                    self.data[param] = TT1TimeSeries(file=file)

    def __repr__(self):
        text = f"TT-1 Pulse #{self.pulse} data."
        return text

    @property
    def B_t(self):
        """
        Toroidal field in T.

        Returns
        -------
        B_t : DataFrame
            Toroidal Field in T as function of time.

        """
        B_t = 1.165 * self.data["IT2"].df / self.R ** (1.1) / 1e4
        return pd.DataFrame(B_t).rename(columns={"IT2 [A]": "B_t [T]"})

    @property
    def I_p(self):
        """
        Plasma Current in A.

        Returns
        -------
        I_p : DataFrame
            Plasma Current in A as function of time.

        """
        return self.data["IP2"].df.rename(columns={"IP2 [A]": "I_p [A]"})

    @property
    def q_a(self):
        """
        Edge Safety Factor.

        q_a = 2 pi a^2/R Bt/Ip

        Returns
        -------
        q_a : DataFrame
            Edge safety factor as function of time.

        """
        mu0 = 4 * np.pi * 1e-7
        q_a = (
            2
            * np.pi
            * self.a**2
            / (self.R * mu0)
            * self.B_t["B_t [T]"]
            / self.I_p["I_p [A]"]
        )

        return pd.DataFrame(q_a, columns=["q_a"])

    @property
    def duration(self):
        """
        Plasma duration.

        The plasma duration is defined by Ip>1000A.

        Returns
        -------
        duration : float
            Plasma duration.

        """
        plasma = self.I_p.loc[self.I_p["I_p [A]"] > 1e3]
        duration = plasma.index[-1] - plasma.index[0]
        return duration

    @property
    def df(self):
        """
        Return the pulse time series data as a pandas DataFrame.

        Returns
        -------
        df : pandas.DataFrame
            DataFrame which contains all the time series data.

        """
        df = pd.concat([d.df for (param, d) in self.data.items()], axis=1)
        # add some processed data
        df = pd.concat([df, self.B_t, self.I_p, self.q_a], axis=1)
        return df
