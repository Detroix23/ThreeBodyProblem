"""
# Gravity.
src/gravity_detroix23/physics/grid.py
"""
import math
from typing import TYPE_CHECKING

import pyxel

if TYPE_CHECKING:
    from gravity_detroix23.app.board import Board
from gravity_detroix23.physics.vectors import Vector2D, Size
from gravity_detroix23.modules import scene_objects
from gravity_detroix23.physics.points import Point
from gravity_detroix23.app import drawing


class Grid(scene_objects.SceneObject):
    """
    Represent the space-time grid
    """
    def __init__(
        self, 
        frequency: float, 
        zoom_dependence: bool, 
        force_weight: float, 
        color_grid: int, 
        color_point: int, 
        board: 'Board',
    ) -> None:
        self.frequency: float = frequency
        self.zoom_dependence: bool = zoom_dependence
        self.color_grid: int = color_grid
        self.color_point: int = color_point
        self.board: 'Board' = board
        self.force_weight: float = force_weight
        self.force_exponent: float = 0.5
        # Use lists index to find neighbors, Point cords to draw lines
        self.points: list[list[Point]] = []
        return

    def update(self) -> None:
        """
        Fill the `self.points` `list[list[Point]]` by computing each point. 
        """
        self.points = []
        
        d = Size(
            int(math.floor(float(self.board.width)  / self.frequency)),
            int(math.floor(float(self.board.height) / self.frequency)),
        )

        for y in range(0, self.board.height + 2 * d.y, d.y):
            points_x: list[Point] = []
            for x in range(0, self.board.width + 2 * d.x, d.x):
                # Screen position
                point: Point = Point(
                    Vector2D(x - d.x, y - d.y),
                    board=self.board
                )
                point.force = Vector2D(0, 0)
                # Check G-Force for all bodies
                for target in self.board.system.values():
                    target_force: Vector2D = point.gravitational_force_from(target.position, target.mass)
                    # Tweak the display force.
                    force_value: float = target_force.magnitude()
                    target_force.normalize()
                    target_force.multiply(pow(force_value, self.force_exponent) * self.force_weight)
                    point.force.x += target_force.x
                    point.force.y += target_force.y
                
                if self.board.grid_move_point:
                    point.position.x += int(point.force.x)
                    point.position.y += int(point.force.y)
                    
                points_x.append(point)
            self.points.append(points_x)

        return

    def draw(self) -> None:
        """
        Draw the whole grid.
        """
        points_y: list[list[Point]] = self.points

        i: int = 0
        while i < len(points_y):
            j: int = 0
            points_x: list[Point] = points_y[i]
            while j < len(points_x):
                point: Point = points_x[j]
                # Draw points
                drawing.draw_point(point.position.x, point.position.y, color=self.color_point)
                if not self.board.grid_move_point:
                    point.force.draw_on(point.position.x, point.position.y, 1, color=10)
                else:
                    # Draw grid lines, if there are points (facing +y, then to +x)
                    if i + 1 < len(points_y):
                        pyxel.line(
                            point.position.x, 
                            point.position.y, 
                            points_y[i + 1][j].position.x, 
                            points_y[i + 1][j].position.y, 
                            col=self.color_grid
                        )
                    if j + 1 < len(points_x):
                        pyxel.line(
                            point.position.x, 
                            point.position.y, 
                            points_x[j + 1].position.x, 
                            points_x[j + 1].position.y, 
                            col=self.color_grid
                        )
                
                j += 1
            i += 1

        return
    