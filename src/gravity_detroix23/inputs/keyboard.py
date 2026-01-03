"""
# Gravity.  
src/gravity_detroix23/inputs/keyboard.py  
"""

import pyxel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from gravity_detroix23.app import board

class Buttons:
	"""
	Manage user presses.  
	Uses mainly `pyxel.btn` method.   
	"""
	board: 'board.Board'

	def __init__(self, board: 'board.Board') -> None:
		self.board = board

	def listen(self) -> None:
		"""
		Listen to user inputs
		"""
		# Time controls
		if pyxel.btnr(pyxel.KEY_SPACE) and self.board.times.speed != 0:
			self.board.times.speed_previous = self.board.times.speed
			self.board.times.frame_per_frame_previous = self.board.times.frame_per_frame
			self.board.times.speed = 0
			self.board.times.frame_per_frame = 9999999
		elif pyxel.btnr(pyxel.KEY_SPACE):
			self.board.times.speed = self.board.times.speed_previous
			self.board.times.frame_per_frame = self.board.times.frame_per_frame_previous

		elif pyxel.btn(pyxel.KEY_1):
			self.board.times.speed = 0.1
			self.board.times.frame_per_frame = 1
		elif pyxel.btn(pyxel.KEY_2):
			self.board.times.speed = 0.5
			self.board.times.frame_per_frame = 2
		elif pyxel.btn(pyxel.KEY_3):
			self.board.times.speed = 1
			self.board.times.frame_per_frame = 5
		elif pyxel.btn(pyxel.KEY_4):
			self.board.times.speed = 2
			self.board.times.frame_per_frame = 10
		elif pyxel.btn(pyxel.KEY_5):
			self.board.times.speed = 4
			self.board.times.frame_per_frame = 20
		elif pyxel.btn(pyxel.KEY_6):
			self.board.times.speed = 10
			self.board.times.frame_per_frame = self.board.fps

		# Zoom
		if pyxel.btn(pyxel.KEY_PAGEUP):
			self.board.camera.zoom -= 0.05 * self.board.camera.zoom
			self.board.camera.update()

		elif pyxel.btn(pyxel.KEY_PAGEDOWN):
			self.board.camera.zoom += 0.05 * self.board.camera.zoom
			self.board.camera.update()

		elif pyxel.btn(pyxel.KEY_HOME):
			self.board.camera.reset()

		# Camera position
		if pyxel.btn(pyxel.KEY_LEFT):
			self.board.camera.position.x -= int(10 / self.board.camera.zoom)
		elif pyxel.btn(pyxel.KEY_RIGHT):
			self.board.camera.position.x += int(10 / self.board.camera.zoom)
		if pyxel.btn(pyxel.KEY_DOWN):
			self.board.camera.position.y += int(10 / self.board.camera.zoom)
		elif pyxel.btn(pyxel.KEY_UP):
			self.board.camera.position.y -= int(10 / self.board.camera.zoom)

		# Displays
		if pyxel.btnr(pyxel.KEY_G):
			self.board.draw_grid = not self.board.draw_grid
		elif pyxel.btnr(pyxel.KEY_E):
			self.board.draw_elements = not self.board.draw_elements
		elif pyxel.btnr(pyxel.KEY_R):
			self.board.draw_force = not self.board.draw_force
		elif pyxel.btnr(pyxel.KEY_T):
			self.board.draw_text = not self.board.draw_text
		elif pyxel.btnr(pyxel.KEY_F):
			self.board.draw_velocity = not self.board.draw_velocity
		elif pyxel.btnr(pyxel.KEY_Y):
			self.board.draw_trails = not self.board.draw_trails
