"""
THREE BODY PROBLEM
Settings and enumeration file
"""
from enum import Enum
from pathlib import Path

from modules.maths_local import *

# Gravity
class Edge(Enum):
    NONE = 1
    HARD = 2
    BOUNCE = 3
    TOR = 4
    
class SimMode(Enum):
    RANDOM = 1
    CONFIG = 2
    DEFAULT = 3 

class CollisionsBehaviour(Enum):
    NONE = 1
    COLLIDE = 2
    COLLIDE_WITH_FUSION = 3
    COLLIDE_WITH_BUMP = 4


