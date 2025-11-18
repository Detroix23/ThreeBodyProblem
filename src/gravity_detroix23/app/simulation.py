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

class Board:
    """
    # Board.
    Runs the game, display elements, listen to player inputs.
    """
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
        # Vars
        self.exponent_softener: float = exponent_softener    
        self.gravitational_constant: float = gravitational_constant
        self.mass_softener: float = mass_softener      
        self.edges: settings.Edge = edges
        self.width: int = width
        self.height: int = height
        self.title: str = title
        self.fps: int = fps
        self.bounce_factor: float = bounce_factor
        self.collisions: settings.CollisionsBehaviour = collisions
        # Controls
        self.camera: Vector2D = Vector2D(0, 0)
        self.zoom: float = 1
        self.time_speed: float = 0
        self.time_speed_previous: float = 1
        self.frame_per_frame: int = 9999999
        self.frame_per_frame_previous: int = 1

        # UI
        self.draw_elems: bool = True
        self.draw_velocity: bool = draw_velocity
        self.draw_force: bool = draw_force
        self.draw_text: bool = draw_text
        self.draw_grid: bool = draw_grid
        self.draw_trails: bool = True

        # Grid
        self.grid_frequency: int = 16
        self.grid_force_weight: float = 2.3
        # True to move the points, False to fix the point but show the vectors
        self.grid_move_point: bool = not grid_draw_vector
        self.grid_color_grid: int = 10
        self.grid_color_point: int = 11

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
            self.grid_frequency, 
            False, 
            self.grid_force_weight, 
            self.grid_color_grid, 
            self.grid_color_point, 
            board = self
        )

    def user_inputs(self) -> None:
        """
        Listen to user inputs
        """
        # Time controls
        if pyxel.btnr(pyxel.KEY_SPACE) and self.time_speed != 0:
            self.time_speed_previous = self.time_speed
            self.frame_per_frame_previous = self.frame_per_frame
            self.time_speed = 0
            self.frame_per_frame = 9999999
        elif pyxel.btnr(pyxel.KEY_SPACE):
            self.time_speed = self.time_speed_previous
            self.frame_per_frame = self.frame_per_frame_previous

        elif pyxel.btn(pyxel.KEY_1):
            self.time_speed = 0.1
            self.frame_per_frame = 1
        elif pyxel.btn(pyxel.KEY_2):
            self.time_speed = 0.5
            self.frame_per_frame = 2
        elif pyxel.btn(pyxel.KEY_3):
            self.time_speed = 1
            self.frame_per_frame = 5
        elif pyxel.btn(pyxel.KEY_4):
            self.time_speed = 2
            self.frame_per_frame = 10
        elif pyxel.btn(pyxel.KEY_5):
            self.time_speed = 4
            self.frame_per_frame = 20
        elif pyxel.btn(pyxel.KEY_6):
            self.time_speed = 10
            self.frame_per_frame = self.fps

        # Zoom
        if pyxel.btn(pyxel.KEY_PAGEUP) and self.zoom > 0.0:
            self.zoom -= 0.05 * self.zoom
            #self.width = int(self.width * self.zoom)
            #self.height = int(self.height * self.zoom)
        elif pyxel.btn(pyxel.KEY_PAGEDOWN) and self.zoom < 15.0:
            self.zoom += 0.05 / self.zoom
            #self.width = int(self.width * self.zoom)
            #self.height = int(self.height * self.zoom)
        elif pyxel.btn(pyxel.KEY_HOME):
            self.zoom = 1
            self.camera.x = 0
            self.camera.y = 0
            pyxel.camera()

        # Camera position
        if pyxel.btn(pyxel.KEY_LEFT):
            self.camera.x -= int(10 / self.zoom)
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.camera.x += int(10 / self.zoom)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.camera.y += int(10 / self.zoom)
        elif pyxel.btn(pyxel.KEY_UP):
            self.camera.y -= int(10 / self.zoom)

        # Displays
        if pyxel.btnr(pyxel.KEY_G):
            self.draw_grid = not self.draw_grid
        elif pyxel.btnr(pyxel.KEY_E):
            self.draw_elems = not self.draw_elems
        elif pyxel.btnr(pyxel.KEY_R):
            self.draw_force = not self.draw_force
        elif pyxel.btnr(pyxel.KEY_T):
            self.draw_text = not self.draw_text
        elif pyxel.btnr(pyxel.KEY_F):
            self.draw_velocity = not self.draw_velocity
        elif pyxel.btnr(pyxel.KEY_Y):
            self.draw_trails = not self.draw_trails

    def update(self) -> None:
        """
        Update simulation
        """
        # Debug
        if self.first_update:
            print("- Game running")
            self.first_update = not self.first_update
        
        # Inputs
        self.user_inputs()
        # Grid
        if self.draw_grid:
            self.grid_main.generate_points()
        # Frame limiter for the game
        if pyxel.frame_count % self.frame_per_frame == 0:      
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
        pyxel.camera(self.camera.x, self.camera.y)
       
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
                element.force_vector.draw_on(x = element.position.x, y = element.position.y, size=1, color=3) 
            if self.draw_velocity:
                element.velocity.draw_on(x = element.position.x, y = element.position.y, size=1, color=5)
            

