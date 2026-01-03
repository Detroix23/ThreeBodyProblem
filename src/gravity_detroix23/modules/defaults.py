"""
# Gravity.
/gravity/src/modules/default.py  
"""
from typing import Final

from gravity_detroix23.modules import (
	settings,
	types
)


SPRITE_COLKEY: Final[int] = 8

class APP:
	TITLE: str = "Simulation"
	BOARD_WIDTH: int  = 1000
	BOARD_HEIGHT: int = 1000
	FPS: int = 25

	G: float = (6.67*(10**2))
	EDGE: settings.Edge = settings.Edge.NONE
	BOUNCE_FACTOR: float = 1.0
	MASS_SOFTENER: float = 1.0
	EXPONENT_SOFTENER: float = -0.0
	DRAW_VELOCITY: bool = True
	DRAW_FORCE: bool = False
	DRAW_TEXT: bool = True
	DRAW_GRID: bool = True
	COLLISIONS: settings.CollisionsBehavior = settings.CollisionsBehavior.COLLIDE_WITH_FUSION
	GRID_DRAW_VECTORS: bool = False
	DEFAULT_MODE: settings.SimMode = settings.SimMode.DEFAULT 

def app_dict() -> dict[str, types.setting]:
	"""
	Return a cleaned `dict` of the default `APP` settings.
	"""
	return {name: value for name, value in APP.__dict__.items() if not name.startswith("_")}
 