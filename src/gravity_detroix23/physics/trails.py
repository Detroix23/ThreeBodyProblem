"""
# Gravity.
src/gravity/physics/trails.py  
"""

import pyxel
from typing import Optional

from gravity_detroix23.physics import maths 
from gravity_detroix23.modules import console

class Trail:
	"""
	Store the positions of an element, and allow to draw a line of its movement.
	"""
	positions: list[maths.Vector2D]
	length: int
	color: int

	def __init__(
		self, 
		length: int,
		color: int,
		*,
		positions: Optional[list[maths.Vector2D]] = None,
	) -> None:
		"""
		Construct a trail.  
		Use the `position` if you want to manually create a path.
		"""
		self.positions = positions if positions else []
		self.length = length
		self.color = color

	def __repr__(self) -> str:
		return f"Trail(length={self.length}, color={self.color}, positions={console.pretty(self.positions, end=" ")})"

	@property
	def first(self) -> maths.Vector2D:
		"""
		Return the first position.  
		If no positions have been tracked, return a (0, 0) vector.   
		"""
		if self.positions:
			return self.positions[0]
		else:
			return maths.Vector2D(0, 0)

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
