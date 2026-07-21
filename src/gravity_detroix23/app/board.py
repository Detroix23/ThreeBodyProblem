"""
# Gravity.
src/gravity/app/simulation.py  
"""

import pyxel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gravity_detroix23.app.app import App

from gravity_detroix23.inputs import keyboard
from gravity_detroix23.physics.vectors import Vector2D
from gravity_detroix23.modules import scene_objects, settings, console
from gravity_detroix23.physics import collisions, element, grids
from gravity_detroix23.app import controls

class Board(scene_objects.SceneObject):
    """
    # Board.
    Runs the game, display elements, listen to player inputs.
    """
    app: 'App'
    buttons: keyboard.Buttons
    camera: controls.Camera
    times: controls.Time
    frames: int

    def __init__(
        self, 
        app: 'App',
        system: dict[str, settings.InputElement], 
        width: int, 
        height: int, 
        title: str, 
        fps: int, 
        gravitational_constant: float, 
        edges: settings.Edge, 
        bounce_factor: float,  
        mass_softener: float, 
        exponent_softener: float,
        collisions: settings.CollisionsBehavior,
        grid_draw_vector: bool,
        draw_velocity: bool = True, 
        draw_force: bool = True, 
        draw_text: bool = True, 
        draw_grid: bool = True,
    ) -> None:
        """
        Initialize the game.
        """
        self.app = app
        self.frames = 0
        self.exponent_softener: float = exponent_softener    
        self.gravitational_constant: float = gravitational_constant
        self.mass_softener: float = mass_softener      
        self.width: int = width
        self.height: int = height
        self.title: str = title
        self.fps: int = fps
        self.bounce_factor: float = bounce_factor
        self.edges: settings.Edge = edges
        self.collisions: settings.CollisionsBehavior = collisions

        # Workers
        self.buttons = keyboard.Buttons(self)
        self.camera = controls.Camera(self)
        self.times = controls.Time(self)

        # UI
        self.draw_elements: bool = True
        self.draw_velocity: bool = draw_velocity
        self.draw_force: bool = draw_force
        self.draw_text: bool = draw_text
        self.draw_grid: bool = draw_grid
        self.draw_trails: bool = True

        # True to move the points, False to fix the point but show the vectors
        self.grid_move_point: bool = not grid_draw_vector

        # Elements
        self.system: dict[str, element.Element] = {
            element_name: element.Element(
                self, 
                mass=element_stats.mass,
                position=element_stats.position,
                name=element_stats.name,
                size=element_stats.size,
                velocity=element_stats.velocity,
            )
            for element_name, element_stats in system.items()
        }

        print("- Provided system: ")
        print(console.pretty(system))
        print("- Saved system: ")
        print(console.pretty(self.system))

        # Grid
        self.grid_main: grids.Grid = grids.Grid(
            frequency=16, 
            zoom_dependence=False, 
            force_weight=2.3, 
            color_grid=pyxel.COLOR_YELLOW, 
            color_point=pyxel.COLOR_GREEN, 
            board=self,
        )
        return

    def update(self) -> None:
        """
        Update simulation
        """
        self.frames += 1

        # Inputs
        self.buttons.update()

        # Grid
        if self.draw_grid:
            self.grid_main.update()

        # Frame limiter for the game
        if not self.times.frame_skip():      
            # Interactions for each element, all elements.
            for element_main in self.system.values():
                element_main.force_vector = Vector2D(0, 0)
                for element_target in self.system.values():
                    collisions.interaction(element_main, element_target, self.collisions)
                
            # Move
            for element in self.system.values():
                element.update()
                element.collisions = []
        
        return
        
    def draw(self) -> None:
        """
        Draw all simulation
        """
        # Clear all
        pyxel.cls(0)

        # Camera
        self.camera.update()
       
        # Trails.
        if self.draw_trails:
            for element in self.system.values():
                element.trail.draw()

        # Grid
        if self.draw_grid:
            self.grid_main.draw()

        # All elements, layer 2.
        for element in self.system.values():
            position: Vector2D

            if self.draw_elements:
                element.draw()
            if self.draw_force:
                position = self.app.simulation.camera.transform(element.position.copy())
                element.force_vector.draw_on(position.x, position.y, size=1, color=3) 
            if self.draw_velocity:
                position = self.app.simulation.camera.transform(Vector2D(element.position.x, element.position.y))
                element.velocity.draw_on(position.x, position.y, size=1, color=5)
            
        return

