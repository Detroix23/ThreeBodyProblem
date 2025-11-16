"""
# Gravity.
/gravity/src/modules/default.py  
"""
from typing import Final

from gravity.modules import (
	types,
	settings,
)


TITLE: str = "Simulation"
BOARD_WIDTH: int  = 1000
BOARD_HEIGHT: int = 1000
FPS: int = 25

G: float = (6.67*(10**2))
EDGE: settings.Edge = settings.Edge.NONE
BOUNCE_FACTOR: float = 1.0
MASS_SOFTENER: float = 1.0
EXPONENENT_SOFTENER: float = -0.0
DRAW_VELOCITY: bool = True
DRAW_FORCE: bool = False
DRAW_TEXT: bool = True
DRAW_GRID: bool = True
COLLISIONS: settings.CollisionsBehaviour = settings.CollisionsBehaviour.COLLIDE_WITH_FUSION
GRID_DRAW_VECTORS: bool = False
DEFAULT_MODE: settings.SimMode = settings.SimMode.DEFAULT 

APP: Final[dict[str, types.setting]] = {
	"TITLE": "Simulation",
	"BOARD_WIDTH": 1000,
	"BOARD_HEIGHT": 1000,
	"FPS": 25,
	"G": 6.67*(10**2),
	"EDGE": settings.Edge.NONE,
	"BOUNCE_FACTOR": 1.0,
	"MASS_SOFTENER": 1.0,
	"EXPONENENT_SOFTENER": 0.0,
	"DRAW_VELOCITY": True,
	"DRAW_FORCE": False,
	"DRAW_TEXT": True,
	"DRAW_GRID": True,
	"COLLISIONS": settings.CollisionsBehaviour.COLLIDE_WITH_FUSION,
	"GRID_DRAW_VECTORS": False,
	"DEFAULT_MODE": settings.SimMode.DEFAULT,
}
