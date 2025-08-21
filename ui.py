"""
THREE BODY PROBLEM
User configs
Run: 2nd
"""
import random

from maths_local import *
import main
import modules.settings as settings


# dict[str, tuple[int, tuple[int, int], str, int, tuple[float, float]]]
class InputElem:
    """
    Named tuple of the input infos.
    """
    def __init__(self, mass: int, position: Vector2D, name: str, size: int, velocity: Vector2D) -> None:
        self.mass: int = mass
        self.position: Vector2D = position
        self.name: str = name
        self.size: int = size
        self.velocity: Vector2D = velocity

    def __repr__(self) -> str:
        return f"{self.__class__!s}({self.__dict__!r})"
    
    def __str__(self) -> str:
        return f"Elem: {self.name}, position: x={self.position.x}, y={self.position.y}, size={self.size}, velocity: x={self.velocity.x}, y={self.velocity.y}"




def listing_input(text: str, allowed: str = 'int') -> str:
    listening: list[str] = ['q', 'quit']
    input_result = input(text)
    for i in range(1, len(listening)):
        if input_result.strip().lower() == listening[i]:
            raise ValueError('Exit')
    try:
        if allowed == 'str':
            str(input_result)
        elif allowed == 'int':
            int(input_result)
    except Exception:
        raise

    return input_result


class Layers:
    """
    Define what things and layers to show. 
    """
    def __init__(self, elems: bool, grid: bool, hud: bool) -> None:
        self.elems: bool = elems
        self.grid: bool = grid
        self.hud: bool = hud
        


def app_cmd() -> dict[str, InputElem]:
    """
    Basic starting sequence for the user, in CMD.
    """
    print("# Three body problem simulations")
    ## Config
    user_mode_str: str = input(f"Please select a mode {"{rand/conf/default}"}[{main.DEFAULT_MODE}]: ")
    system_input: dict[str, InputElem] = {}

    if user_mode_str in ["r", "rand", "random"]:
        user_mode: settings.SimMode = settings.SimMode.RANDOM
    elif user_mode_str in ["d", "def", "default"]:
        user_mode: settings.SimMode = settings.SimMode.DEFAULT
    elif user_mode_str in ["c", "con", "conf", "config"]:
        user_mode: settings.SimMode = settings.SimMode.CONFIG
    else:
        user_mode: settings.SimMode = main.DEFAULT_MODE
        print(f"(!) - Incorrect input; set to '{main.DEFAULT_MODE}'")
        

    if user_mode == settings.SimMode.RANDOM:
        print("# Mode selected: rand (random generation)")
        number_elements: int = random.randint(3, 5)
        border_coverage: float = 0.2
        borders: dict[str, int] = {
            "West": int(main.BOARD_WIDTH * border_coverage),
            "East": int(main.BOARD_WIDTH * (1 - border_coverage)),
            "North": int(main.BOARD_HEIGHT * border_coverage),
            "South": int(main.BOARD_HEIGHT * (1 - border_coverage))
        }
        weight_min: int = 100
        weight_max: int = 10000
        velocity_x_max: float = 1.5
        velocity_y_max: float = 1.5
        velocity_x_min: float = -1.5
        velocity_y_min: float = -1.5
        
        i: int = 1
        while i <= number_elements:
            name_random: str = "Plan" + str(i)
            mass_random: int = random.randint(weight_min, weight_max)
            position_x_random = random.randint(borders["West"], borders["East"])
            position_y_random = random.randint(borders["North"], borders["South"])
            system_input[name_random] = InputElem(
                mass_random, 
                Vector2D(position_x_random, position_y_random), 
                name_random, 
                int(mass_random / 100), 
                Vector2D(random.uniform(velocity_x_min, velocity_x_max), random.uniform(velocity_y_min, velocity_y_max))
            )
            i += 1

    elif user_mode == settings.SimMode.CONFIG:
        user_exit: bool = False
        print("# Mode selected: conf (manual configuration);")
        while not user_exit:
            if system_input: print("Currently loaded: ")
            for element in system_input:
                print("- " + element)

            print("New element: respect type, 'q' to validate to launch")
            manual: dict[str, str] = {}
            try:
                manual['name'] = listing_input("- Name (str): ", allowed='str')
                manual['mass'] = listing_input("- Mass (int): ")
                manual['position_x'] = listing_input("- Starting position (x): ")
                manual['position_y'] = listing_input("- Starting position (y): ")

                system_input[manual['name']] = InputElem(
                    int(manual['mass']), Vector2D(float(manual['position_x']), float(manual['position_y'])), manual['name'], int(int(manual['mass']) / 100), Vector2D(0, 0)
                )
            except ValueError as e:
                if e.__str__() == 'Exit':
                    user_exit = True
                    print("Choice validated.")
                else:
                    print("(!) - Value error; input anew.\n")

            except Exception as e:
                print(f"(?) - Something else went wrong ({str(e)}). Enter anew element.\n")

    else:
        if not user_mode_str:
            print("# Mode selected: [default] (use default value)")
        else:
            print("# Mode selected: default (use default value)")

        system_input["Plan1"] = InputElem(10500, Vector2D(445, 560), "Plan1", int(10500 / 100), Vector2D(0, 0))
        system_input["Plan2"] = InputElem(400, Vector2D(580, 450), "Plan2", int(400 / 100), Vector2D(0, 10))
        system_input["Plan3"] = InputElem(300, Vector2D(400, 400), "Plan3", int(300 / 100), Vector2D(0, 10))
        system_input["Plan4"] = InputElem(300, Vector2D(300, 350), "Plan4", int(300 / 100), Vector2D(0, 10))

    # Warnings (!)
    if not system_input:
        print("# (!) - Empty system.")
    elif len(system_input) == 1:
        print("# (!) - One element system.")

    # Sorting the element by size. 
    # system_input = {elems for elems in sorted(system_input.items(), key=lambda item: item[1].size)}
    
    print("Starting...")

    # Completion.
    return system_input

if __name__ == "__main__":
    print("THREE BODY PROBLEM - Libraries.")
    print("UI.")