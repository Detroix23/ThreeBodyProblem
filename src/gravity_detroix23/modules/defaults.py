"""
# Gravity.
/gravity/src/modules/default.py  
"""
from typing import Final

from gravity_detroix23.modules import (
	settings,
	typings
)

SPRITE_COLKEY: Final[int] = 8

DEFAULT_MODE: settings.SimMode = settings.SimMode.DEFAULT 

class App:
	width: int = 1000
	height: int = 1000
	title: str = "Simulation"
	fps: int = 25
	gravitational_constant: float = (6.67*(10**2))
	edges: settings.Edge = settings.Edge.NONE
	bounce_factor: float = 1.0
	mass_softener: float = 1.0
	exponent_softener: float = -0.0
	collisions: settings.CollisionsBehavior = settings.CollisionsBehavior.COLLIDE_WITH_FUSION
	grid_draw_vector: bool = False
	draw_velocity: bool = True
	draw_force: bool = False
	draw_text: bool = True
	draw_grid: bool = True

	@classmethod
	def to_dict(cls) -> dict[str, typings.setting]:
		"""
		Return a cleaned `dict` of the default `App` settings.
		"""
		return {
			name: value 
			for name, value in cls.__dict__.items() 
			if not (name.startswith("_") or name.startswith("to_"))
		}

 