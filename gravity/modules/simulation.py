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
import modules.drawing as drawing

# GUI
class Board:
    def __init__(
        self, 
        system: dict[str, ui.InputElem], 
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
        Args:
            @edges (string): {none, hard, bounce, tor}
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
        
        # Grid
        self.grid_frequency: int = 16
        self.grid_force_weight: float = 2.3
        # True to move the points, False to fix the point but show the vectors
        self.grid_move_point: bool = not grid_draw_vector
        self.grid_color_grid: int = 10
        self.grid_color_point: int = 11

        # Debug
        self.first_update = True

        # Elements
        self.system: dict[str, Elem] = {}
        for element_name, element_stats in system.items():
            self.system[element_name] = Elem(
                self, 
                mass = element_stats.mass,
                position = element_stats.position,
                name = element_stats.name,
                size = element_stats.size,
                velocity = element_stats.velocity
            )
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
            for elemMain in self.system.values():
                elemMain.force_vector = Vector2D(0, 0)
                for elemTarget in self.system.values():
                    if elemMain != elemTarget:
                        distance: float = elemMain.distance_to(elemTarget)
                        if distance > (elemMain.size / 2 + elemTarget.size / 2):
                            target_force: Vector2D = elemMain.gravitational_force_from(elemTarget)
                            elemMain.force_vector.add(target_force)
                        elif self.collisions in [settings.CollisionsBehaviour.COLLIDE, settings.CollisionsBehaviour.COLLIDE_WITH_FUSION, settings.CollisionsBehaviour.COLLIDE_WITH_BUMP]:
                            collision(elemMain, elemTarget, behaviour=self.collisions)
            
            # Move
            for elem in self.system.values():
                elem.move()
                elem.collisions = [] # type: ignore
        
        
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
        # All elems
        for _, elem in self.system.items():
            if self.draw_elems:
                elem.draw()
            if self.draw_force:
                elem.force_vector.draw_on(x = elem.position.x, y = elem.position.y, size=1, color=3) 
            if self.draw_velocity:
                elem.velocity.draw_on(x = elem.position.x, y = elem.position.y, size=1, color=5)
        
        
            

class Elem:
    """
    Define a stellar element
    """
    CHECK_RADIUS: int = 100
    SPRITE_POSITION: Vector2D = Vector2D(16, 0)
    SPRITE_SIZE: Vector2D = Vector2D(16, 16)
    SPRITE_IMAGE: int = 0
    SPRITE_COLKEY: int = 0
    SPRITE_SIZE_FACTOR: float = 1/16

    def __init__(
        self, 
        BOARD: Board, 
        mass: int, 
        position: Vector2D, 
        velocity: Vector2D,
        color: int = 5, 
        size: int = 2, 
        name: str = "",
    ) -> None:
        """
        Creation of the elem, with "mass, vInit, xStart, yStart, color=5, size=2".
        """
        self.BOARD: Board = BOARD
        self.mass: float = mass  
        self.position: Vector2D = position

        self.displacement: Vector2D = Vector2D(0, 0)        
        self.velocity: Vector2D = velocity
        self.force_vector: Vector2D = Vector2D(x = 0, y = 0)
        self.collisions: list[Self] = []

        # Drawing sprite will use the pyxres template, else, a square will be drawn.
        self.draw_sprite: bool = True
        self.size: int = size
        self.color: int = color
        self.name: str = name

    def __str__(self) -> str:
        return f"Elem {self.name} - Position: x={self.position.x}; y={self.position.y}, Mass: m={self.mass}, Force: x={self.force_vector.x}; y={self.force_vector.y}."
    
    def __repr__(self) -> str:
        return f"Elem {self.name} - Position: x={self.position.x}; y={self.position.y}, Mass: m={self.mass}, Force: x={self.force_vector.x}; y={self.force_vector.y}."
    
    def distance_to(self, target: Self) -> float:
        """
        Compute distance between this elem and the target elem
        """
        return math.sqrt((target.position.x - self.position.x) ** 2 + (target.position.y - self.position.y) ** 2)
    
    def gravitational_force_from(self, target: Self) -> Vector2D:
        """
        Find the gravitational force vector
        """
        direction: int = 1
        # Direction
        vector_distance: Vector2D = Vector2D(x = target.position.x - self.position.x, y = target.position.y - self.position.y)
        vector_distance.normalize()
        # Distance
        distance: float = self.distance_to(target)
        # Limit artifically distance and prevent division by 0
        distance_min: float = ((self.size + 1) / 2 + (target.size + 1) / 2)
        if distance < distance_min:
            distance = distance_min
        
        # F force value
        force: float = (self.BOARD.gravitational_constant * target.mass) / (distance ** (2 + self.BOARD.exponent_softener))
        # Force vector
        vector_force: Vector2D = Vector2D(x = force * vector_distance.x * direction, y = force * vector_distance.y * direction)
        # Watch for overshot of planets
        velocity_next: Vector2D = Vector2D(
            x = self.velocity.x + self.force_vector.x / (self.mass * self.BOARD.mass_softener),
            y = self.velocity.y + self.force_vector.y / (self.mass * self.BOARD.mass_softener)
        )
        if velocity_next.magnitude >= distance:
            direction = -1
            velocity_next_magnitude: float = velocity_next.magnitude
            velocity_next.normalize()
            velocity_next.mult((velocity_next_magnitude - distance) * direction)
        
        
        return vector_force


    def move(self) -> None:
        """
        Move the elem, according to force vector at a scale (mass) and checking collision
        """ 
        # Apply force
        self.velocity = Vector2D(
            x = self.velocity.x + self.force_vector.x / (self.mass * self.BOARD.mass_softener),
            y = self.velocity.y + self.force_vector.y / (self.mass * self.BOARD.mass_softener)
        )
        # Apply velocity
        self.position = Vector2D(
            x = self.position.x + self.velocity.x,
            y = self.position.y + self.velocity.y
        )
         # Apply optional displacement
        self.position.add(self.displacement)
        # Check edges
        """ Disabled for now """
        # Reset values
        self.displacement = Vector2D(0, 0)

    def draw(self) -> None:
        """
        Draw itself on the board
        """
        
        # Draw on computed values
        size: int = int(self.size)
        position: Vector2D = Vector2D(
            int(self.position.x),
            int(self.position.y)
        )
        if self.draw_sprite:
            pyxel.blt(
                x=self.position.x - (self.size / (2 * self.size * self.SPRITE_SIZE_FACTOR)), 
                y=self.position.y - (self.size / (2 * self.size * self.SPRITE_SIZE_FACTOR)), 
                img=self.SPRITE_IMAGE, 
                u=self.SPRITE_POSITION.x,
                v=self.SPRITE_POSITION.y,
                w=self.SPRITE_SIZE.x,
                h=self.SPRITE_SIZE.y,
                colkey=self.SPRITE_COLKEY,
                scale=self.size * self.SPRITE_SIZE_FACTOR
            )
            # Main rectangle
            pyxel.rect(position.x - 16 / 2, position.y - 16 / 2, 16, 16, col=7)
        else:
            # Main rectangle
            pyxel.rect(position.x - size / 2, position.y - size / 2, size, size, col=self.color)
            # Outline
            pyxel.rectb(position.x - size / 2, position.y - size / 2, size, size, col=7)
        
        # Center
        drawing.draw_point(int(position.x), int(position.y), 16)
    


def collision(a: Elem, b: Elem, behaviour: settings.CollisionsBehaviour) -> bool:
    """
    Collide two elements and change their velocity by inverting the direction and preserving the actual speed.
    To avoid the effect to cancel itself, each Elem has a list of already collided elements.
    Return True if collision actually happened, False otherwise
    """
    collision_state: bool = False
    if a not in b.collisions and b not in a.collisions:   
        # Detroix23 collision simplification 4, using a medium vector n, affected by mass and direction, that reflect the velocity vectors.
        n: Vector2D = a.velocity * a.mass + b.velocity * b.mass
        n.normalize()

        a.velocity = ((n * 2) * (a.velocity.dot(n))) - a.velocity
        b.velocity = ((n * 2) * (b.velocity.dot(n))) - b.velocity

        a.collisions.append(b)
        b.collisions.append(a)
        collision_state = True
        # Check where the elems are going to land.
        distance_min = a.size / 2 + b.size / 2
        future_position_a: Vector2D = a.position + a.velocity
        future_position_b: Vector2D = b.position + b.velocity
        future_distance: float = math.sqrt((future_position_a.x - future_position_b.x) ** 2 + (future_position_a.y - future_position_b.y) ** 2)
        # Try to unclip
        if future_distance < distance_min:
            # Collision unclip.
            v: Vector2D = Vector2D(future_position_b.x - future_position_a.x, future_position_b.y - future_position_a.y)
            d: float = v.magnitude
            v.normalize()
            displacement: Vector2D = v * (a.size / 2 - d + b.size / 2)
            n_a: float = - b.mass / (a.mass + b.mass)
            n_b: float = a.mass / (a.mass + b.mass)

            a.displacement = Vector2D(displacement.x, displacement.y) * n_a
            b.displacement = Vector2D(displacement.x, displacement.y) * n_b
            # print(f"! C - Fu: {a.displacement=} {n_a}, {b.displacement=} {n_b}; ")
    return collision_state
    