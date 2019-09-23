# -*- coding: utf-8 -*-
from enum import Enum, auto


class State(Enum):
    ACTIVE = auto()
    DONE = auto()
    INVALID = auto()
