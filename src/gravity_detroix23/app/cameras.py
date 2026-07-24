"""
# Gravity.  
src/gravity_detroix23/app/cameras.py    
"""
from typing import TYPE_CHECKING, Callable

import pyxel

if TYPE_CHECKING:
	from gravity_detroix23.app.board import Board
from gravity_detroix23.physics.vectors import Vector2D
from gravity_detroix23.modules import scene_objects
from gravity_detroix23.modules.keys import KeyBinding, KeySensitive, Trigger

class Camera(scene_objects.Updatable, KeySensitive):
    """
    Controls the app's camera.
    """
    board: 'Board'
    position: Vector2D
    zoom: float
    bindings: list[KeyBinding]

    def __init__(self, board: 'Board') -> None:
        self.board = board
        self.position = Vector2D(0, 0)
        self.zoom = 1
        self.bindings = [
            KeyBinding(pyxel.KEY_PAGEUP, "Camera: zoom in.",    self.zoom_factory(-0.05)),
            KeyBinding(pyxel.KEY_PAGEDOWN, "Camera: zoom out.", self.zoom_factory(0.05)),
            KeyBinding(pyxel.KEY_HOME, "Camera: reset.", self.reset),
            KeyBinding(pyxel.KEY_RIGHT, "Camera: right.", self.move_factory(Vector2D(-10.0, 0.0))),
            KeyBinding(pyxel.KEY_LEFT, "Camera: left.",   self.move_factory(Vector2D(10.0,  0.0))),
            KeyBinding(pyxel.KEY_UP, "Camera: up.",       self.move_factory(Vector2D(0.0,   10.0))),
            KeyBinding(pyxel.KEY_DOWN, "Camera: down.",   self.move_factory(Vector2D(0.0,  -10.0))),
            KeyBinding(pyxel.KEY_G, "Camera: toggle grid", self.toggle_draw_grid, Trigger.RELEASED),
            KeyBinding(pyxel.KEY_E, "Camera: toggle elements", self.toggle_draw_elements, Trigger.RELEASED),
            KeyBinding(pyxel.KEY_R, "Camera: toggle force", self.toggle_draw_force, Trigger.RELEASED),
            KeyBinding(pyxel.KEY_T, "Camera: toggle text", self.toggle_draw_text, Trigger.RELEASED),
            KeyBinding(pyxel.KEY_F, "Camera: toggle velocity", self.toggle_draw_velocity, Trigger.RELEASED),
            KeyBinding(pyxel.KEY_Y, "Camera: toggle trails", self.toggle_draw_trails, Trigger.RELEASED),
        ] 
        return
    
    def zoom_factory(self, amount: float) -> Callable[[], None]:
        """
        Create zoom functions that update zoom according to `amount`.
        """
        def zoom() -> None:
            self.zoom += amount * self.board.camera.zoom
            self.update()

        return zoom

    def move_factory(self, vector: Vector2D) -> Callable[[], None]:
        """
        Create move functions that displaces the camera by `vector`.
        """
        def move() -> None:
            self.position += vector

        return move

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
        other: Vector2D, 
        inverted: bool = False,
    ) -> Vector2D:
        """
        Apply camera shift and zoom, creating a new copy `Vector2D` from an `other` `Vector2D`.
        """
        if inverted:
            return (other / self.zoom) - self.position	
        else:
            return (other + self.position) * self.zoom

    def toggle_draw_grid(self) -> None:
        """
        Toggle _on_ and _off_ the flag variable `draw_grid`.
        """
        self.board.draw_grid = not self.board.draw_grid
        return

    def toggle_draw_elements(self) -> None:
            """
            Toggle _on_ and _off_ the flag variable `draw_elements`.
            """
            self.board.draw_elements = not self.board.draw_elements
            return

    def toggle_draw_force(self) -> None:
            """
            Toggle _on_ and _off_ the flag variable `draw_force`.
            """
            self.board.draw_force = not self.board.draw_force
            return

    def toggle_draw_text(self) -> None:
            """
            Toggle _on_ and _off_ the flag variable `draw_text`.
            """
            self.board.draw_text = not self.board.draw_text
            return

    def toggle_draw_velocity(self) -> None:
            """
            Toggle _on_ and _off_ the flag variable `draw_velocity`.
            """
            self.board.draw_velocity = not self.board.draw_velocity
            return

    def toggle_draw_trails(self) -> None:
            """
            Toggle _on_ and _off_ the flag variable `draw_trails`.
            """
            self.board.draw_trails = not self.board.draw_trails
            return

    def get_bindings(self) -> list[KeyBinding]:
        return self.bindings
    