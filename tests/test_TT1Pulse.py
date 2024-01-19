# -*- coding: utf-8 -*-
import pytest
from TT1.pulse import TT1Pulse


def test_wrong_pulse_number():
    'Test using a wrong pulse number.'
    with pytest.raises(FileExistsError):
        TT1Pulse(-1)

def test_dummy_pulse():
    'Read default time series for a pulse.'
    pulse = TT1Pulse(0)
    
    df = pulse.df
    
def test_readall_pulse():
    'Read all time series for a pulse.'
    pulse = TT1Pulse(0, read_all=True)
    
    df = pulse.df