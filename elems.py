"""
THREE BODY PROBLEM
Definitions of elements
"""

#Local
import main


class Elem:
    """
    Define a stellar element
    """
    CHECK_RADIUS = 100
    
    def __init__(
        self, BOARD: main.Board, mass: int, position: tuple[float, float], force_vector: tuple[float, float] = (0, 0), velocity: float = 0,
        color: int = 5, size: int = 2, name: str = ""
    ) -> None:
        """
        Creation of the elem, with "mass, vInit, xStart, yStart, color=5, size=2".
        """
        self.BOARD: main.Board = BOARD
        self.mass: float = mass
        self.velocity: float = velocity
        self.position: tuple[float, float] = position
        
        self.force_vector: tuple[float, float] = force_vector

        self.size: int = size
        self.color: int = color
        self.name: str = name

    def __str__(self) -> str:
        return f"Elem {self.name} - Position: x={self.position[0]}; y={self.position[1]}, Mass: m={self.mass}, Force: x={self.force_vector[0]}; y={self.force_vector[1]}."
    
    def __repr__(self) -> str:
        return f"Elem {self.name} - Position: x={self.position[0]}; y={self.position[1]}, Mass: m={self.mass}, Force: x={self.force_vector[0]}; y={self.force_vector[1]}."
    
    def distance_to(self, target) -> float:
        """
        Compute distance between this elem and the target elem
        """
        return main.math.sqrt((self.position[0] - target.position[0]) ** 2 + (self.position[1] - target.position[1]) ** 2)
    
    def gravitational_force_from(self, target) -> tuple[float, float]:
        """
        Find the gravitational force vector
        """
        # Direction
        vector_distance: tuple[float, float] = (self.position[0] - target.position[0], self.position[1] - target.position[1])
        theta = main.math.atan2(vector_distance[1], vector_distance[0])          ### Radians
        ## theta_deg = math.degrees(theta)
        # Distance (limited)
        distance: float = self.distance_to(target)
        if distance < ((self.size + 1) / 2 + (target.size + 1) / 2):
            distance = ((self.size + 1) / 2 + (target.size + 1) / 2)
        # F force value
        force: float = (self.BOARD.gravitational_constant * target.mass) / (distance ** (2 + self.BOARD.exponent_softener))
        # Force vector
        ### Rectification because we go anti-trigonometric way, clockwise.
        vector_force: tuple[float, float] = (force * -main.math.cos(theta), force * -main.math.sin(theta))

        return vector_force

    def does_collide_with(self, target) -> bool:
        return False

    def move(self) -> None:
        """
        Move the elem, according to force vector at a scale (mass) and checking collision
        """
        # Force
        self.position = (
            self.position[0] + (self.force_vector[0] / (self.mass * self.BOARD.mass_softener + 1) * self.BOARD.time_speed),
            self.position[1] + (self.force_vector[1] / (self.mass * self.BOARD.mass_softener + 1) * self.BOARD.time_speed)
        )

        # Check edges
        ## New for version
        for axis1 in (0, 1):
            axis2: int = abs(axis1 - 1)
            force_vector_list: list[float] = list(self.force_vector)
            position_list: list[float] = list(self.position)

            if self.position[axis1] + self.size / 2 >= self.BOARD.width:
                if self.BOARD.edges == "bounce":
                    force_vector_list[axis1] = self.force_vector[axis1] * -self.BOARD.bounce_factor
                    force_vector_list[axis2] = self.force_vector[axis2]
                    ### Force it to be in the board and count reflexion
                    position_list[axis1] = 2 * self.BOARD.width - self.size / 2 - self.position[axis1]

                elif self.BOARD.edges == "hard":
                    force_vector_list[axis1] = 0.0
                    force_vector_list[axis2] = self.force_vector[axis2]
                    ### Force it to be in the board
                    position_list[axis1] = self.BOARD.width - self.size / 2
                    
            elif self.position[axis1] <= 0:
                if self.BOARD.edges == "bounce":
                    force_vector_list[axis1] = self.force_vector[axis1] * -self.BOARD.bounce_factor
                    force_vector_list[axis2] = self.force_vector[axis2]
                    ### Force it to be in the board and count reflexion
                    position_list[axis1] = 0

                elif self.BOARD.edges == "hard":
                    force_vector_list[axis1] = 0.0
                    force_vector_list[axis2] = self.force_vector[axis2]
                    ### Force it to be in the board
                    position_list[axis1] = 0


            self.force_vector = (force_vector_list[0], force_vector_list[1])
            self.position = (position_list[0], position_list[1])

    def draw(self) -> None:
        """
        Draw itself on the board
        """
        # Draw on computed values
        size: int = int(self.size * self.BOARD.zoom)
        position_x: int = int((self.position[0] + self.BOARD.camera_x) * self.BOARD.zoom)
        position_y: int = int((self.position[1] + self.BOARD.camera_y) * self.BOARD.zoom)

        main.pyxel.rect(position_x - size / 2, position_y - size / 2, size, size, col=self.color)
        main.pyxel.rect(position_x, position_y, 1, 1, col=self.color + 1)





if __name__ == "__main__":
    print("THREE BODY PROBLEM - Libraries.")
    print("Elems.")
