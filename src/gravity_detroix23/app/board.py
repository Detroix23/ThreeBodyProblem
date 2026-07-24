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
from gravity_detroix23.physics import element, grids
from gravity_detroix23.app import cameras, times

class Board(scene_objects.SceneObject):
    """
    # Board.
    Runs the game, display elements, listen to player inputs.
    """
    app: 'App'
    frames: int
    exponent_softener: float
    gravitational_constant: float
    mass_softener: float
    width: int
    height: int
    title: str
    fps: int
    bounce_factor: float
    edges: settings.Edge
    collisions: settings.CollisionsBehavior
    system: dict[int, element.Element]
    buttons: keyboard.Buttons
    camera: cameras.Camera
    times: times.Time
    draw_elements: bool
    draw_velocity: bool
    draw_force: bool
    draw_text: bool
    draw_grid: bool
    draw_trails: bool
    grid_move_point: bool

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
        self.exponent_softener = exponent_softener    
        self.gravitational_constant = gravitational_constant
        self.mass_softener = mass_softener      
        self.width = width
        self.height = height
        self.title = title
        self.fps = fps
        self.bounce_factor = bounce_factor
        self.edges = edges
        self.collisions = collisions

        # Workers
        self.buttons = keyboard.Buttons(self)
        self.camera = cameras.Camera(self)
        self.times = times.Time(self)

        # UI
        self.draw_elements = True
        self.draw_velocity = draw_velocity
        self.draw_force = draw_force
        self.draw_text = draw_text
        self.draw_grid = draw_grid
        self.draw_trails = True

        # True to move the points, False to fix the point but show the vectors
        self.grid_move_point = not grid_draw_vector

        # Elements
        self.system = {
            index: element.Element(
                self, 
                mass=stats.mass,
                id=index,
                position=stats.position,
                name=stats.name,
                size=stats.size,
                velocity=stats.velocity,
            )
            for index, (_, stats) in enumerate(system.items())
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

    def next_free_id(self) -> int:
        """
        Get next free `int` ID for the elements `system`'s.
        """
        last: int = max(self.system.keys())
        index: int = 0
        while index < last:
            if last not in self.system.keys():
                last = index 
            index += 1

        return last + 1

    def update(self) -> None:
        """
        Update simulation.
        """
        self.frames += 1

        # 1. Inputs.
        self.buttons.update()

        # 2. Grid.
        if self.draw_grid:
            self.grid_main.update()

        # 3. Elements.
        for element in self.system.values():
            element.update()
        
        return
        
    def draw(self) -> None:
        """
        Draw all simulation.
        """
        pyxel.cls(0)
        self.camera.update()

        # 1. Trails.
        if self.draw_trails:
            for element in self.system.values():
                element.trail.draw()

        # 2. Grid
        if self.draw_grid:
            self.grid_main.draw()

        # 3. All elements.
        for element in self.system.values():
            position: Vector2D

            if self.draw_elements:
                element.draw()
            
            if self.draw_force:
                position = self.app.simulation.camera.transform(element.position.copy())
                element.acceleration.draw_on(
                    position.x, 
                    position.y, 
                    size=1, 
                    color=pyxel.COLOR_RED,
                ) 
            
            if self.draw_velocity:
                position = self.app.simulation.camera.transform(element.position.copy())
                element.velocity.draw_on(
                    position.x, 
                    position.y, 
                    size=1, 
                    color=pyxel.COLOR_LIGHT_BLUE,
                )
            
        return
