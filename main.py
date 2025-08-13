"""
THREE BODY PROBLEM
Simulation of planet movement
Use of gravitational formula: F = (m1*m2) / d**2
We consider that all elements are spherical
"""

# Imports
import math
import random
## Representation
#import matplotlib.pyplot as plt
import pyxel
# Local
import elems
import ui

# Types
## type vect = tuple[float, float]

class Vec2D:
    """
    Define a simple 2D vector with methods
    """
    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y
        
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self) -> None:
        magnitude: float = self.magnitude()
        self.x = self.x / magnitude
        self.y = self.y/ magnitude
        
        assert(self.magnitude != 1)
    
        
        

# Simulation
# GUI
class Board:
    def __init__(
        self, system: dict[str, tuple], width: int = 128, height: int = 128, title: str = "Simulation", fps: int = 30, 
        edges: str = "none", mass_softener: float = 1000.0,
        gravitational_constant: float = (10**-11), exponent_softener: float = 0.0, bounce_factor: float = 1.0,
    ) -> None:
        """
        Initialize the game.
        Args:
            @edges (string): {none, hard, bounce, tor}
        """
        # Vars
        ### Distance expoential softener
        self.exponent_softener: float = exponent_softener    
        self.gravitational_constant: float = gravitational_constant
        ### Mass factor
        self.mass_softener: float = mass_softener      
        self.edges: str = edges
        self.width: int = width
        self.height: int = height
        self.title: str = title
        self.fps: int = fps
        self.bounce_factor: float = bounce_factor

        # Controls
        self.camera_x: int = 0
        self.camera_y: int = 0
        self.zoom: float = 1
        self.time_speed: float = 0
        self.time_speed_previous: float = 1

        # Text
        self.texts_main: list[str] = [
            ""
        ]

        # Debug
        self.first_update = True

        # Init elements
        ## Elements
        self.system: dict[str, elems.Elem] = {}
        
        for element_name, element_stats in system.items():
            self.system[element_name] = elems.Elem(
                self, 
                mass=element_stats[0],
                position=element_stats[1],
                name=element_stats[2],
                size=element_stats[3],
                force_vector=element_stats[4]
            )
        
        
        print("- Provided system: ")
        print(system)
        print("- Saved system: ")
        print(self.system)
        
        ## Representation
        ### Positions

        self.elemsX: list[float] = []
        self.elemsY: list[float] = []
        # print("## Initialization of the elements: ")
        for name, elem in self.system.items():
            self.elemsX.append(elem.position[0])
            self.elemsY.append(elem.position[1])
            # print("-", elem)

        # Init simulation screen
        pyxel.init(width=width, height=height, title=title, fps=fps)
        print("- Pyxel board initialized")
        
        # Run
        pyxel.run(self.update, self.draw)
        print("# Game ended")

    def user_inputs(self) -> None:
        """
        Listen to user inputs
        """
        # Time controls
        if pyxel.btn(pyxel.KEY_SPACE) and self.time_speed != 0:
            self.time_speed_previous = self.time_speed
            self.time_speed = 0
        elif pyxel.btn(pyxel.KEY_SPACE):
            self.time_speed = self.time_speed_previous

        elif pyxel.btn(pyxel.KEY_1):
            self.time_speed = 0.1
        elif pyxel.btn(pyxel.KEY_2):
            self.time_speed = 0.5
        elif pyxel.btn(pyxel.KEY_3):
            self.time_speed = 1
        elif pyxel.btn(pyxel.KEY_4):
            self.time_speed = 2
        elif pyxel.btn(pyxel.KEY_5):
            self.time_speed = 4
        elif pyxel.btn(pyxel.KEY_6):
            self.time_speed = 10

        # Zoom
        if pyxel.btn(pyxel.KEY_PAGEUP) and self.zoom > 0.0:
            self.zoom -= 0.05 * self.zoom
            #self.width = int(self.width * self.zoom)
            #self.height = int(self.height * self.zoom)
        elif pyxel.btn(pyxel.KEY_PAGEDOWN) and self.zoom < 15.0:
            self.zoom += 0.05
            #self.width = int(self.width * self.zoom)
            #self.height = int(self.height * self.zoom)

        # Camera position
        if pyxel.btn(pyxel.KEY_LEFT):
            self.camera_x -= int(10 / self.zoom)
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.camera_x += int(10 / self.zoom)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.camera_y += int(10 / self.zoom)
        elif pyxel.btn(pyxel.KEY_UP):
            self.camera_y -= int(10 / self.zoom)

    def text_main(self, text_color: int = 8) -> None:
        x = y = 10
        self.texts_main = [
            "# Three Body Problem - title=" + self.title + "; edges=" + self.edges + ", fps=" + str(self.fps) + ", frames=" + str(pyxel.frame_count),
            "- Controls: zoom=" + str(self.zoom) + ", camera: x=" + str(self.camera_x) + "; y=" + str(self.camera_y) + "",
            "- Time: speed=" + str(self.time_speed) + "",
            "- Elements: total=" + str(len(self.system)) + "",
            "---"
        ]
        for txt in self.texts_main:
            pyxel.text(x, y, txt, text_color)
            y += 6

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

        # Calc interactions
        ## Check for each element, all elements.
        for elemMain in self.system.values():
            elemMain.force_vector = (0, 0)
            # print(elemMain.name, ":", elemMain.forceVector[0], elemMain.forceVector[1], end=" - ")
            for elemTarget in self.system.values():
                if elemMain != elemTarget:
                    target_force: tuple[float, float] = elemMain.gravitational_force_from(elemTarget)
                    elemMain.force_vector = (
                        elemMain.force_vector[0] + target_force[0],
                        elemMain.force_vector[1] + target_force[1]
                    )
        # print()
        # Move
        for elem in self.system.values():
            elem.move()

    def draw(self) -> None:
        """
        Draw all simulation
        """
        # Clear all
        pyxel.cls(0)
        # All elems
        for name, elem in self.system.items():
            elem.draw()

        # Text
        self.text_main()




def mean(vect: list[float]) -> float:
    """
    Compute vector mean
    """
    return math.sqrt((vect[0]**2) + (vect[1]**2))


# Run
if __name__ == "__main__":
    
    ui.app_cmd()

    print("---\nEnd")




