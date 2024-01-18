# -*- coding: utf-8 -*-
"""
Example of usage of the TT1 module.
"""
#%% imports
from TT1.pulse import TT1Pulse
import matplotlib.pyplot as plt

#%% Plot time series for a given pulse
pulse = TT1Pulse(2466)

fig, axes = plt.subplots(3, 1, sharex=True)
pulse.I_p.plot(ax=axes[0])
pulse.B_t.plot(ax=axes[1])
pulse.q_a.plot(ax=axes[2])
axes[0].set_xlim(330, 345)
axes[2].set_ylim(0, 100)

#%% Another way of plotting things
fig, ax = plt.subplots()
pulse.df[['IP1 [A]', 'IP2 [A]']].plot(ax=ax)

#%% Get the edge safety factor at max Ip for a few pulses
pulse_nbs = [2463, 2464, 2465, 2466]
results = {}

for pulse_nb in pulse_nbs:
    pulse = TT1Pulse(pulse_nb)
    results[pulse_nb] = pulse.q_a.loc[pulse.I_p.idxmax()]

print(results)

#%% Plasma Duration for all shots located in the data dir
from pathlib import Path
datadir = Path('data').absolute()
pulse_nbs = []
for pulsepath in datadir.glob('24*'):
    pulse_nbs.append(int(str(pulsepath).split("\\")[-1]))

durations = {}
for pulse_nb in pulse_nbs:
    try: 
        durations[pulse_nb] = TT1Pulse(pulse_nb).duration
    except IndexError as e:  # no plasma
        durations[pulse_nb] = 0
    
print(durations)

