"""
THREE BODY PROBLEM
Settings and enumeration file
"""

from modules.maths_local import *
from enum import Enum

class Edge(Enum):
    NONE = 1
    HARD = 2
    BOUNCE = 3
    TOR = 4
    
class SimMode(Enum):
    RANDOM = 1
    CONFIG = 2
    DEFAULT = 3 

# Pyxel
RESSOURCE_FILE: str = "./assets/gravity.pyxres"