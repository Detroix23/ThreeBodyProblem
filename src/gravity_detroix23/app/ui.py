"""
# Three body problem.
src/gravity_detroix23/app/ui.py
"""

import random

from gravity_detroix23.physics.maths import Vector2D
from gravity_detroix23.modules import defaults, settings

class Layers:
    """
    Define what things and layers to show. 
    """
    def __init__(self, elements: bool, grid: bool, hud: bool) -> None:
        self.elements: bool = elements
        self.grid: bool = grid
        self.hud: bool = hud
        

def listing_input(text: str, allowed: str = 'int') -> str:
    listening: list[str] = ['q', 'quit']
    input_result: str = input(text)
    for i in range(1, len(listening)):
        if input_result.strip().lower() == listening[i]:
            raise ValueError('Exit')

    if allowed == 'str':
        str(input_result)
    elif allowed == 'int':
        int(input_result)

    return input_result

def app_cmd() -> dict[str, settings.InputElement]:
    """
    Basic starting sequence for the user, in CMD.
    """
    ## Config
    user_mode_str: str = input(f"Please select a mode (rand|conf|default)[{defaults.APP.DEFAULT_MODE}]: ")
    user_mode: settings.SimMode
    system_input: dict[str, settings.InputElement] = {}

    if user_mode_str in {"r", "rand", "random"}:
        user_mode = settings.SimMode.RANDOM
    elif user_mode_str in {"d", "def", "default"}:
        user_mode = settings.SimMode.DEFAULT
    elif user_mode_str in {"c", "con", "conf", "config"}:
        user_mode = settings.SimMode.CONFIG
    else:
        user_mode = defaults.APP.DEFAULT_MODE
        
    if user_mode == settings.SimMode.RANDOM:
        print("-> `rand` (random generation).")
        number_elements: int = random.randint(3, 5)
        border_coverage: float = 0.2
        borders: dict[str, int] = {
            "West": int(defaults.APP.BOARD_WIDTH * border_coverage),
            "East": int(defaults.APP.BOARD_WIDTH * (1 - border_coverage)),
            "North": int(defaults.APP.BOARD_HEIGHT * border_coverage),
            "South": int(defaults.APP.BOARD_HEIGHT * (1 - border_coverage))
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
            position_x_random: int = random.randint(borders["West"], borders["East"])
            position_y_random: int = random.randint(borders["North"], borders["South"])
            system_input[name_random] = settings.InputElement(
                mass_random, 
                Vector2D(position_x_random, position_y_random), 
                name_random, 
                int(mass_random / 100), 
                Vector2D(random.uniform(velocity_x_min, velocity_x_max), random.uniform(velocity_y_min, velocity_y_max))
            )
            i += 1

    elif user_mode == settings.SimMode.CONFIG:
        user_exit: bool = False
        print("-> `conf` (manual configuration).")
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

                system_input[manual['name']] = settings.InputElement(
                    int(manual['mass']), 
                    Vector2D(float(manual['position_x']), float(manual['position_y'])), 
                    manual['name'], 
                    int(int(manual['mass']) / 100), 
                    Vector2D(0, 0),
                )
            except ValueError as exception:
                if exception.__str__() == 'Exit':
                    user_exit = True
                    print("Choice validated.")
                else:
                    print("(!) app.ui.app_cmd() Value error; input anew.\n")

            except Exception as e:
                print(f"(?) app.ui.app_cmd() Something else went wrong ({str(e)}). Retry.\n")

    else:
        if not user_mode_str:
            print("-> [`default`] (use default value).")
        else:
            print("-> `default` (use default value).")

        system_input = settings.DEFAULT_SYSTEM

    # Warnings.
    if not system_input:
        print("# (!) app.ui.app_cmd() Empty system.")
    elif len(system_input) == 1:
        print("# (!) app.ui.app_cmd() One element system.")

    # Sorting the element by size. 
    system_input = {
        element[0]: element[1]
        for element in sorted(system_input.items(), key=lambda item: item[1].size)
    }

    # Completion.
    return system_input
