"""
# Gravity.  
src/gravity_detroix23/inputs/mouse.py    
"""

import pyxel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from gravity_detroix23.app.app import App

from gravity_detroix23.physics import element, vectors
from gravity_detroix23.modules import defaults, scene_objects


class Mouse(scene_objects.SceneObject):
	"""
	# Mouse
	Draw cursor and allow interaction.
	"""
	SPRITE_IMAGE: int = 0
	TEMPLATE_POSITION: vectors.Size = vectors.Size(32, 0)
	TEMPLATE_SIZE: vectors.Size = vectors.Size(16, 16)
	SPRITE_COLKEY: int = defaults.SPRITE_COLKEY
	MOUSE_BODY_NAME: str = "[Mouse body]"

	app: 'App'
	size: float
	show: bool
	mouse_element: element.Element

	def __init__(
		self, 
		app: 'App',
		size: float, 
		show: bool = True,
	) -> None:
		self.app = app
		self.size = size
		self.show = show
		self.mouse_element = element.Element(
			board=self.app.simulation,
			mass=100,
			position=vectors.Vector2D(0, 0),
			velocity=vectors.Vector2D(0, 0),
			size=0,
			name=self.MOUSE_BODY_NAME,
			trail_size=0,
		)

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

	def update(self) -> None:
		"""
		Listen to mouse actions.
		"""
		if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
			self.update_mouse_body()
		elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
			self.delete_mouse_body()
		
		if pyxel.mouse_wheel != 0:
			self.app.simulation.camera.zoom += pyxel.mouse_wheel * 0.05 * self.app.simulation.camera.zoom

		return
	
	def update_mouse_body(self) -> None:
		"""
		Create or update the mouse body
		"""
		if Mouse.MOUSE_BODY_NAME not in self.app.simulation.system.keys():
			self.app.simulation.system[Mouse.MOUSE_BODY_NAME] = self.mouse_element
		self.app.simulation.system[Mouse.MOUSE_BODY_NAME].position = self.app.simulation.camera.transform(
			vectors.Vector2D(pyxel.mouse_x, pyxel.mouse_y), True
		)

		return
	
	def delete_mouse_body(self) -> None:
		"""
		Remove the `mouse_element` from the simulation's system.
		"""
		self.app.simulation.system.pop(Mouse.MOUSE_BODY_NAME)
	