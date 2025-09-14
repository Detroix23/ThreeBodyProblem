"""
THREE BODY PROBLEM
GUI
Run 3rd
"""

import pyxel
from typing_extensions import Self

from modules.maths_local import *
import modules.ui as ui
import modules.settings as settings
import modules.grid as grid
import modules.element as element
import modules.collisions as collisions
import modules.camera as camera
import modules.drawing as drawing

# GUI
class Board():
    def __init__(
        self, 
        system: list[settings.InputElem], 
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
        self.collisions = collisions
        # Controls
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
        
        # Grid
        self.grid_frequency: int = 16
        self.grid_force_weight: float = 2.3
        # True to move the points, False to fix the point but show the vectors
        self.grid_move_point: bool = not grid_draw_vector
        self.grid_color_grid: int = 10
        self.grid_color_point: int = 11

        # Debug
        self.first_update: bool = True

        # Camera
        self.camera: camera.Camera = camera.Camera(self)

        # Elements
        self.system: list[element.Element] = []
        for elem in system:
            self.system.append(element.Element(
                self, 
                mass = elem.mass,
                position = elem.position,
                name = elem.name,
                size = elem.size,
                velocity = elem.velocity
            ))
        print("- Provided system: ")
        print(system)
        print("- Saved system: ")
        print(self.system)

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
        if pyxel.btn(pyxel.KEY_PAGEUP) and self.camera.zoom > 0.0:
            self.camera.zoom -= 0.05 * self.camera.zoom
            #self.width = int(self.width * self.zoom)
            #self.height = int(self.height * self.zoom)
        elif pyxel.btn(pyxel.KEY_PAGEDOWN) and self.camera.zoom < 15.0:
            self.camera.zoom += 0.05 / self.camera.zoom
            #self.width = int(self.width * self.zoom)
            #self.height = int(self.height * self.zoom)
        elif pyxel.btn(pyxel.KEY_HOME):
            self.camera.zoom = 1
            self.camera.position.x = 0
            self.camera.position.y = 0
            pyxel.camera()

        # Camera position
        if pyxel.btn(pyxel.KEY_LEFT):
            self.camera.position.x -= int(10 / self.camera.zoom)
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.camera.position.x += int(10 / self.camera.zoom)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.camera.position.y += int(10 / self.camera.zoom)
        elif pyxel.btn(pyxel.KEY_UP):
            self.camera.position.y -= int(10 / self.camera.zoom)

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
            for elemMain in self.system:
                elemMain.force_vector = Vector2D(0, 0)
                for elemTarget in self.system:
                    if elemMain != elemTarget:
                        distance: float = elemMain.distance_to(elemTarget)
                        if distance > (elemMain.size / 2 + elemTarget.size / 2):
                            target_force: Vector2D = elemMain.gravitational_force_from(elemTarget)
                            elemMain.force_vector.add(target_force)
                        elif self.collisions in [
                            settings.CollisionsBehaviour.COLLIDE, 
                            settings.CollisionsBehaviour.COLLIDE_WITH_FUSION, 
                            settings.CollisionsBehaviour.COLLIDE_WITH_BUMP
                        ]:
                            collisions.collision(elemMain, elemTarget, behaviour=self.collisions)
            
            # Move
            for elem in self.system:
                elem.move()
                elem.collisions = [] # type: ignore


        
    def draw(self) -> None:
        """
        Draw all simulation
        """
        # Clear all
        pyxel.cls(0)
        # Camera
        pyxel.camera(self.camera.position.x, self.camera.position.y)
        # Grid
        if self.draw_grid:
            self.grid_main.draw()
        # All elems
        for elem in self.system:
            if self.draw_elems:
                elem.draw()
            if self.draw_force:
                elem.force_vector.draw_on(x = elem.position.x, y = elem.position.y, size=1, color=3) 
            if self.draw_velocity:
                elem.velocity.draw_on(x = elem.position.x, y = elem.position.y, size=1, color=5)

