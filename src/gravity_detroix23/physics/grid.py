"""
THREE BODY PROBLEM.
Grid.
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gravity_detroix23.app import simulation
from gravity_detroix23.physics.maths import *
from gravity_detroix23.app import drawing

class Point:
    """
    Point of the grid 
    """
    
    def __init__(self, x: int, y: int, board: 'simulation.Board') -> None:
        self.x: int = x
        self.y: int = y
        self.BOARD: 'simulation.Board' = board
        self.force: Vector2D = Vector2D(0, 0)
        
        
    def distance_to(self, target_position: Vector2D) -> float:
        """
        Compute distance between this elem and the target elem
        """
        return math.sqrt((target_position.x - self.x) ** 2 + (target_position.y - self.y) ** 2)
    
    def gravitational_force_from(self, target_position: Vector2D, target_mass: float) -> Vector2D:
        """
        Find the gravitational force vector
        """
        direction: int = 1
        # Direction
        vector_distance: Vector2D = Vector2D(x = target_position.x - self.x, y = target_position.y - self.y)
        vector_distance.normalize()
        # Distance
        distance: float = self.distance_to(target_position)
        if distance < 1:
            distance = 1
        
        # F force value
        force: float = (self.BOARD.gravitational_constant * target_mass) / (distance ** (2 + self.BOARD.exponent_softener))
        if force > distance:
            force = distance
        # Force vector
        vector_force: Vector2D = Vector2D(x = force * vector_distance.x * direction, y = force * vector_distance.y * direction)
        
        
        return vector_force


class Grid:
    """
    Represent the space-time grid
    """
    def __init__(
        self, 
        frequency: float, 
        zoom_dependance: bool, 
        force_weight: float, 
        color_grid: int, 
        color_point: int, 
        board: 'simulation.Board',
    ) -> None:
        self.frequency: float = frequency
        self.zoom_dependance: bool = zoom_dependance
        self.color_grid: int = color_grid
        self.color_point: int = color_point
        self.board: 'simulation.Board' = board
        self.force_weight: float = force_weight
        self.force_exponent: float = 0.5
        # Use lists index to find neighbours, Point cords to draw lines
        self.points: list[list[Point]] = []
    
    def generate_points(self) -> None:
        self.points = [[]]
        
        dx: int = int(float(self.board.width)  / self.frequency)
        dy: int = int(float(self.board.height) / self.frequency)
        
        
        for y in range(
            int(self.board.camera.y), 
            self.board.height + 2 * dy + int(self.board.camera.y),
            dy
        ):
            points_x: list[Point] = []
            for x in range(
                int(self.board.camera.x), 
                self.board.width + 2 * dx + int(self.board.camera.x), 
                dx
            ):
                point: Point = Point(
                    x - dx,
                    y - dy, 
                    board=self.board
                )
                point.force = Vector2D(0, 0)
                # Check G-Force for all bodies
                for elemTarget in self.board.system.values():
                    target_force: Vector2D = point.gravitational_force_from(elemTarget.position, elemTarget.mass)
                    # Tweak the display force.
                    force_value: float = target_force.magnitude
                    target_force.normalize()
                    target_force.mult(pow(force_value, self.force_exponent) * self.force_weight)
                    point.force.x += target_force.x
                    point.force.y += target_force.y
                
                if self.board.grid_move_point:
                    point.x += int(point.force.x)
                    point.y += int(point.force.y)
                    
                points_x.append(point)
            self.points.append(points_x)


    def draw(self) -> None:
        points_y: list[list[Point]] = self.points
        i: int = 0
        while i < len(points_y):
            j: int = 0
            points_x: list[Point] = points_y[i]
            while j < len(points_x):
                point: Point = points_x[j]
                # Draw points
                drawing.draw_point(point.x, point.y, color=self.color_point)
                if not self.board.grid_move_point:
                    point.force.draw_on(point.x, point.y, 1, color=10)
                else:
                    # Draw grid lines, if there are points (facing +y, then to +x)
                    if i + 1 < len(points_y):
                        pyxel.line(point.x, point.y, points_y[i + 1][j].x, points_y[i + 1][j].y, col=self.color_grid)
                    if j + 1 < len(points_x):
                        pyxel.line(point.x, point.y, points_x[j + 1].x, points_x[j + 1].y, col=self.color_grid)
                j += 1
            i += 1
