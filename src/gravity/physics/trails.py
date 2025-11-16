"""
# Gravity.
src/gravity/physics/trails.py  
"""

import pyxel

from gravity.physics import maths 

class Trail:
	"""
	Store the positions of an element, and allow to draw a line of its movement.
	"""
	positions: list[maths.Vector2D]
	length: int
	color: int

	def __init__(self, length: int, color: int) -> None:
		self.positions = []
		self.length = length
		self.color = color

	def push(self, position: maths.Vector2D) -> None:
		"""
		Add a new point to the beggining of `positions`.  
		Remove if exceeding the `length`.  
		"""
		self.positions.insert(0, position)
		if len(self.positions) >= self.length:
			self.positions.pop()
		
	def draw(self) -> None:
		index: int = 0
		while index < len(self.positions) - 1:
			pyxel.line(
				self.positions[index].x,
				self.positions[index].y,
				self.positions[index + 1].x,
				self.positions[index + 1].y,
				self.color
			)

			index += 1
