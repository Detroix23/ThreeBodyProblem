"""
# Gravity.  
src/gravity_detroix23/app/controls.py    
"""
import pyxel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from gravity_detroix23.app.board import Board
from gravity_detroix23.physics import vectors
from gravity_detroix23.modules import scene_objects

class Camera(scene_objects.Updatable):
	"""
	Controls the app's camera.
	"""
	board: 'Board'
	position: vectors.Vector2D
	zoom: float

	def __init__(self, board: 'Board') -> None:
		self.board = board
		self.position = vectors.Vector2D(0, 0)
		self.zoom = 1
		return

	def update(self) -> None:
		"""
		Update the camera.
		- Move using the `pyxel.camera`.
		- Check bounds.
		"""
		# pyxel.camera(self.position.x, self.position.y)
		if self.zoom < 0.0:
			self.zoom = 0.01

		return

	def reset(self) -> None:
		"""
		Reset the camera to its default settings.
		"""
		self.zoom = 1
		self.position.x = 0
		self.position.y = 0
		# pyxel.camera()
		return

	def transform(
		self, 
		other: vectors.Vector2D, 
		inverted: bool = False,
	) -> vectors.Vector2D:
		"""
		Apply camera shift and zoom, creating a new copy `Vector2D` from an `other` `Vector2D`.
		"""
		if inverted:
			return (other / self.zoom) - self.position	
		else:
			return (other + self.position) * self.zoom



class Time:
	"""
	Control time and execution speed.
	"""
	board: 'Board'
	time_speed: float
	time_speed_previous: float
	frame_per_frame: int
	frame_per_frame_previous: int

	def __init__(self, board: 'Board') -> None:
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
