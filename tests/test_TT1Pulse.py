# -*- coding: utf-8 -*-
import pytest
from TT1.pulse import TT1Pulse


def test_wrong_pulse_number():
    with pytest.raises(FileExistsError):
        TT1Pulse(-1)
