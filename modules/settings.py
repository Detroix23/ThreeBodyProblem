"""
THREE BODY PROBLEM
Settings and enumeration file
"""

from maths_local import *
from enum import Enum

class Edge(Enum):
    NONE = 1
    HARD = 2
    BOUNCE = 3
    TOR = 4
    
class SimMode(Enum):
    RANDOM = 1
    CONFIG = 1
    DEFAULT =1 

