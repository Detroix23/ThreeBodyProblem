"""
# Gravity.  
src/gravity_detroix23/inputs/keyboard.py  
"""

import pyxel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from gravity_detroix23.app.board import Board
from gravity_detroix23.modules import scene_objects

class Buttons(scene_objects.Updatable):
    """
    Manage user presses.  
    Uses mainly `pyxel.btn` method.   
    """
    board: 'Board'

    def __init__(self, board: 'Board') -> None:
        self.board = board
        return

    def update(self) -> None:
        """
        Listen to user inputs
        """
        # Time controls
        self.board.times.update()

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
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.board.camera.position.x -= int(10 / self.board.camera.zoom)
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.board.camera.position.x += int(10 / self.board.camera.zoom)
        if pyxel.btn(pyxel.KEY_UP):
            self.board.camera.position.y += int(10 / self.board.camera.zoom)
        elif pyxel.btn(pyxel.KEY_DOWN):
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

        return
