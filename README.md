# TT1
A Python package to get and analyze the time series data of the Thailand Tokamak 1 (TT1).

## Accessing Data
The data must be stored locally, inside the `data/` directory, with one directory per pulse number. Directory names should be the pulse number.

This package provides a base class `TT1Pulse` which extracts some or all the data from a given pulse number, and additionnaly perform some post-processing operations on signals. 
```
from TT1.pulse import TT1Pulse

pulse = TT1Pulse(2466, read_all=True)
# if read_all=False (default), only some of the signals are read (much faster). If True, *all* the signal files found in the directory are read (slower).
```

The `TT1Pulse` object allows to easily get the time series of the signals, via a pandas DataFrame: `pulse.df`:
```
# one-line plotting
pulse.df.plot(y='IP2 [A]')
```
![image](https://github.com/jhillairet/TT1/assets/4642848/90d65c8f-4d3d-40c6-9acc-f4a8b9fd4f4b)

The list of all the read signals for a pulse can be find in `pulse.df.columns`.
