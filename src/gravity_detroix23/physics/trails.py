"""
# Gravity.
src/gravity/physics/trails.py  
"""

import pyxel
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
	from gravity_detroix23.app.app import App
from gravity_detroix23.physics import vectors 
from gravity_detroix23.modules import console, scene_objects

class Trail(scene_objects.Drawable):
	"""
	Store the positions of an element, and allow to draw a line of its movement.
	"""
	app: 'App'
	positions: list[vectors.Vector2D]
	length: int
	color: int

	def __init__(
		self, 
		app: 'App',
		length: int,
		color: int,
		*,
		positions: Optional[list[vectors.Vector2D]] = None,
	) -> None:
		"""
		Construct a trail.  
		Use the `position` if you want to manually create a path.
		"""
		self.app = app
		self.positions = positions if positions else []
		self.length = length
		self.color = color
		return

	def __repr__(self) -> str:
		return (
			f"Trail(length={self.length}, color={self.color}, "
			f"positions={console.pretty(self.positions, end=' ')})"
		)

	@property
	def first(self) -> vectors.Vector2D:
		"""
		Return the first position.  

		If no positions have been tracked, return a (0, 0) vector.   
		"""
		return (
			self.positions[0]
			if self.positions
			else vectors.Vector2D(0, 0)
		)

	def push(self, position: vectors.Vector2D) -> None:
		"""
		Add a new point to the beginning of `positions`.  

		Remove if exceeding the `length`.  
		"""
		self.positions.insert(0, position)	
		
		if len(self.positions) >= self.length:
			self.positions.pop()

		return

	def draw(self) -> None:
		index: int = 0
		while index < len(self.positions) - 1:
			start: vectors.Vector2D = self.app.simulation.camera.transform(vectors.Vector2D(
				self.positions[index].x,
				self.positions[index].y,
			))
			end: vectors.Vector2D = self.app.simulation.camera.transform(vectors.Vector2D(
				self.positions[index + 1].x,
				self.positions[index + 1].y,
			))
			pyxel.line(
				start.x,
				start.y,
				end.x,
				end.y,
				self.color
			)

			index += 1
		
		return
	