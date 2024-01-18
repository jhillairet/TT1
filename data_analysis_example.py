# -*- coding: utf-8 -*-
"""
Example of usage of the TT1 module.
"""
#%% imports
from TT1.pulse import TT1Pulse
import matplotlib.pyplot as plt

#%% Plot time series for a given pulse
pulse = TT1Pulse(2442)

fig, axes = plt.subplots(3, 1, sharex=True)
pulse.I_p.plot(ax=axes[0])
pulse.B_t.plot(ax=axes[1])
pulse.q_a.plot(ax=axes[2])
axes[0].set_xlim(330, 345)
axes[2].set_ylim(0, 100)

#%% Get the edge safety factor at max Ip for a few pulses
pulse_nbs = [2463, 2464, 2465, 2466]
results = {}

for pulse_nb in pulse_nbs:
    pulse = TT1Pulse(pulse_nb)
    results[pulse_nb] = pulse.q_a.loc[pulse.I_p.idxmax()]

print(results)
# 2463: 47.465025, 
# 2464: 48.718638, 
# 2465: 44.004837, 
# 2466: 58.252482
