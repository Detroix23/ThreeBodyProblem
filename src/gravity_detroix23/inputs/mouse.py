"""
# Gravity.  
src/gravity_detroix23/inputs/mouse.py    
"""

import pyxel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from gravity_detroix23.app import app

from gravity_detroix23.physics import maths
from gravity_detroix23.modules import defaults

class Mouse:
	"""
	# Mouse
	Draw cursor and allow interaction.
	"""
	SPRITE_IMAGE: int = 0
	TEMPLATE_POSITION: maths.Size = maths.Size(32, 0)
	TEMPLATE_SIZE: maths.Size = maths.Size(16, 16)
	SPRITE_COLKEY: int = defaults.SPRITE_COLKEY

	app: 'app.App'
	size: float
	show: bool

	def __init__(
		self, 
		app: 'app.App',
		size: float, 
		show: bool = True,
	) -> None:
		self.app = app
		self.size = size
		self.show = show

	def draw(self) -> None:
		"""
		Draw the mouse cursor, on top of the camera.
		"""
		pyxel.blt(
			x=pyxel.mouse_x,
			y=pyxel.mouse_y,
			img=Mouse.SPRITE_IMAGE,
			u=Mouse.TEMPLATE_POSITION.x,
			v=Mouse.TEMPLATE_POSITION.y,
			w=Mouse.TEMPLATE_SIZE.x,
			h=Mouse.TEMPLATE_SIZE.y,
			colkey=Mouse.SPRITE_COLKEY,
			scale=self.size
		)

