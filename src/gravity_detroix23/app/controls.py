"""
# Gravity.  
src/gravity_detroix23/app/controls.py    
"""
import pyxel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from gravity_detroix23.app import board
from gravity_detroix23.physics import maths

class Camera:
	"""
	Controls the app's camera.
	"""
	board: 'board.Board'
	position: maths.Vector2D
	zoom: float

	def __init__(self, board: 'board.Board') -> None:
		self.board = board
		self.position = maths.Vector2D(0, 0)
		self.zoom = 1

	def update(self) -> None:
		"""
		Move the pyxel camera.
		"""
		pyxel.camera(self.position.x, self.position.y)


class Time:
	"""
	Control time and execution speed.
	"""
	board: 'board.Board'
	time_speed: float
	time_speed_previous: float
	frame_per_frame: int
	frame_per_frame_previous: int

	def __init__(self, board: 'board.Board') -> None:
		self.board = board
		self.speed = 0.0
		self.speed_previous = 1.0
		self.frame_per_frame = 9999999
		self.frame_per_frame_previous = 1

	def frame_skip(self) -> bool:
		"""
		`frame_per_frame` prevent updates on frames not congruent.  
		This method return `True` if this frame is skipped.
		"""
		return pyxel.frame_count % self.frame_per_frame != 0
