"""
# Gravity.
/gravity/src/modules/default.py  
"""
from typing import Final

from gravity_detroix23.modules import settings, typings
from gravity_detroix23.physics.vectors import Vector2D

SPRITE_COLKEY: Final[int] = 8

DEFAULT_MODE: settings.SimMode = settings.SimMode.DEFAULT 

# Defaults.
DEFAULT_SYSTEM: dict[str, settings.InputElement] = {
    # Mass, position, name, size, velocity.
    # system_input["Plan1"] = InputElement(10500, Vector2D(445, 560), "Plan1", 100, Vector2D(0, 0)),
    "Planet2": settings.InputElement(2000, Vector2D(580.0, 450.0), "Planet2", 64, Vector2D(0.0, 50.0)),
    "Planet3": settings.InputElement(1000, Vector2D(400.0, 400.0), "Planet3", 48, Vector2D(0.0, -70.0)),
    #"Planet4": settings.InputElement(200,  Vector2D(300.0, 350.0), "Planet4", 8,  Vector2D(2.0,  0.0)),
}

class App:
	width: int = 1024
	height: int = 1024
	title: str = "Simulation"
	fps: int = 25
	gravitational_constant: float = 6.67 * 10 ** 2
	edges: settings.Edge = settings.Edge.NONE
	bounce_factor: float = 1.0
	mass_softener: float = 1.0
	exponent_softener: float = -0.0
	collisions: settings.CollisionsBehavior = settings.CollisionsBehavior.COLLIDE
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
			if not (name.startswith("_") or name == "to_dict")
		}

 