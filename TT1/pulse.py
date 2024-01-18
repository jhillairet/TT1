import pandas as pd
import numpy as np
from pathlib import Path

from .timeseries import TT1TimeSeries


class TT1Pulse:
    R = 0.6  # major radius in meter
    a = 0.25  # minor radius in meter
    DATA_PATH = "data"
    data_params = {
        "IT2": "Toroidal Current",
        "IP2": "Plasma Current from left-side chamber",
        "GP": "Gas Puffing",
        "HCN1": "HCN Interf HFS",
        "HCN2": "HCN Interf Center",
    }

    def __init__(self, pulse: int):
        self.p = Path(self.DATA_PATH + "/" + str(pulse)).absolute()
        print(self.p)

        if not self.p.exists():
            raise FileExistsError("The specified pulse data do not exist.")

        self.pulse = pulse
        self._read_data(self.p)

    def _read_data(self, path):
        # extract all the data from this pulse
        self.data = {}
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
        return self.data["IP1"].df.rename(columns={"IP1 [A]": "I_p [A]"})

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
            * self.B_t["B_t"]
            / self.I_p["I_p"]
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
        plasma = self.I_p.loc[self.I_p["I_p"] > 1e3]
        duration = plasma.index[-1] - plasma.index[0]
        return duration
