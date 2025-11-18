"""
# Gravity.
src/gravity/app/simulation.py  
"""

import pyxel

from gravity_detroix23.physics.maths import *
from gravity_detroix23.modules import (
	settings,
    console,
)
from gravity_detroix23.physics import (
	collisions, 
	element,
	grid,
)
from gravity_detroix23.app import (
    support,
    inputs,
    controls,
)

class Board:
    """
    # Board.
    Runs the game, display elements, listen to player inputs.
    """
    frames: int
    buttons: inputs.Buttons
    camera: controls.Camera
    times: controls.Time

    def __init__(
        self, 
        system: dict[str, settings.InputElem], 
        width: int, 
        height: int, 
        title: str, 
        fps: int, 
        gravitational_constant: float, 
        edges: settings.Edge, 
        bounce_factor: float,  
        mass_softener: float, 
        exponent_softener: float,
        collisions: settings.CollisionsBehaviour,
        grid_draw_vector: bool,
        draw_velocity: bool = True, 
        draw_force: bool = True, 
        draw_text: bool = True, 
        draw_grid: bool = True,
    ) -> None:
        """
        Initialize the game.
        """
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
        self.collisions: settings.CollisionsBehaviour = collisions

        # Workers
        self.buttons = inputs.Buttons(self)
        self.camera = controls.Camera(self)
        self.times = controls.Time(self)

        # UI
        self.draw_elems: bool = True
        self.draw_velocity: bool = draw_velocity
        self.draw_force: bool = draw_force
        self.draw_text: bool = draw_text
        self.draw_grid: bool = draw_grid
        self.draw_trails: bool = True

        # True to move the points, False to fix the point but show the vectors
        self.grid_move_point: bool = not grid_draw_vector

        # Debug
        self.first_update: bool = True

        # Elements
        self.system: dict[str, element.Element] = {}
        for element_name, element_stats in system.items():
            self.system[element_name] = element.Element(
                self, 
                mass = element_stats.mass,
                position = element_stats.position,
                name = element_stats.name,
                size = element_stats.size,
                velocity = element_stats.velocity
            )
        print("- Provided system: ")
        print(console.pretty(system))
        print("- Saved system: ")
        print(console.pretty(self.system))

        # Grid
        self.grid_main: grid.Grid = grid.Grid(
            frequency=16, 
            zoom_dependance=False, 
            force_weight=2.3, 
            color_grid=support.Color.YELLOW, 
            color_point=support.Color.GREEN, 
            board = self
        )

    def update(self) -> None:
        """
        Update simulation
        """
        # Debug
        if self.first_update:
            print("- Game running")
            self.first_update = not self.first_update
        
        self.frames += 1

        # Inputs
        self.buttons.listen()

        # Grid
        if self.draw_grid:
            self.grid_main.generate_points()

        # Frame limiter for the game
        if not self.times.frame_skip():      
            # Interactions for each element, all elements.
            for element_main in self.system.values():
                element_main.force_vector = Vector2D(0, 0)
                for element_target in self.system.values():
                    if element_main != element_target:
                        distance: float = element_main.distance_to(element_target)
                        if distance > (element_main.size / 2 + element_target.size / 2):
                            target_force: Vector2D = element_main.gravitational_force_from(element_target)
                            element_main.force_vector.add(target_force)
                        elif self.collisions in [
                            settings.CollisionsBehaviour.COLLIDE, 
                            settings.CollisionsBehaviour.COLLIDE_WITH_FUSION, 
                            settings.CollisionsBehaviour.COLLIDE_WITH_BUMP
                        ]:
                            collisions.collision(element_main, element_target, behaviour=self.collisions)
            
            # Move
            for element in self.system.values():
                element.move()
                element.collisions = []
        
        
    def draw(self) -> None:
        """
        Draw all simulation
        """
        # Clear all
        pyxel.cls(0)

        # Camera
        self.camera.update()
       
        # Grid
        if self.draw_grid:
            self.grid_main.draw()
        
        # Trails.
        if self.draw_trails:
            for element in self.system.values():
                element.trail.draw()

        # All elementements, layer 2.
        for element in self.system.values():
            if self.draw_elems:
                element.draw()
            if self.draw_force:
                element.force_vector.draw_on(element.position.x, element.position.y, size=1, color=3) 
            if self.draw_velocity:
                element.velocity.draw_on(element.position.x, element.position.y, size=1, color=5)
            

