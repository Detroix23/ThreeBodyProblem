"""
# Three body problem.
src/gravity_detroix23/app/ui.py
"""
import random
from typing import Type, TypeVar

from gravity_detroix23.physics.vectors import Vector2D
from gravity_detroix23.modules import defaults, settings

class Layers:
    """
    Define what things and layers to show. 
    """
    elements: bool
    grid: bool
    hud: bool

    def __init__(
        self, 
        elements: bool, 
        grid: bool, 
        hud: bool,
    ) -> None:
        self.elements = elements
        self.grid = grid
        self.hud = hud
        
        return


_T_INPUT = TypeVar("_T_INPUT")

def listing_input(
    text: str, 
    allowed: Type[_T_INPUT]
) -> _T_INPUT:
    listening: list[str] = ['q', 'quit']
    input_result: str = input(text)
    for i in range(1, len(listening)):
        if input_result.strip().lower() == listening[i]:
            raise ValueError('Exit')

    return allowed(input_result)   # type: ignore

def app_cmd() -> dict[str, settings.InputElement]:
    """
    Basic starting sequence for the user as a CLI.
    """
    # Config
    user_mode_str: str = input(
        f"Please select a mode (rand|conf|default)[{defaults.DEFAULT_MODE}]: "
    )
    user_mode: settings.SimMode
    system_input: dict[str, settings.InputElement] = {}

    if user_mode_str in {"r", "rand", "random"}:
        user_mode = settings.SimMode.RANDOM
    elif user_mode_str in {"d", "def", "default"}:
        user_mode = settings.SimMode.DEFAULT
    elif user_mode_str in {"c", "con", "conf", "config"}:
        user_mode = settings.SimMode.CONFIG
    else:
        user_mode = defaults.DEFAULT_MODE
        
    if user_mode == settings.SimMode.RANDOM:
        print("-> `rand` (random generation).")
        number_elements: int = random.randint(3, 5)
        border_coverage: float = 0.2
        borders: dict[str, int] = {
            "West": int(defaults.App.width * border_coverage),
            "East": int(defaults.App.width * (1 - border_coverage)),
            "North": int(defaults.App.height * border_coverage),
            "South": int(defaults.App.height * (1 - border_coverage))
        }
        weight_min: int = 100
        weight_max: int = 10000
        velocity_x_max: float = 1.5
        velocity_y_max: float = 1.5
        velocity_x_min: float = -1.5
        velocity_y_min: float = -1.5

        for i in range(number_elements + 1):
            name_random: str = "Plan" + str(i)
            mass_random: int = random.randint(weight_min, weight_max)
            position_x_random: int = random.randint(borders["West"], borders["East"])
            position_y_random: int = random.randint(borders["North"], borders["South"])
            system_input[name_random] = settings.InputElement(
                mass_random, 
                Vector2D(position_x_random, position_y_random), 
                name_random, 
                int(mass_random / 100), 
                Vector2D(
                    random.uniform(velocity_x_min, velocity_x_max), 
                    random.uniform(velocity_y_min, velocity_y_max),
                )
            )

    elif user_mode == settings.SimMode.CONFIG:
        user_exit: bool = False
        print("-> `conf` (manual configuration).")
        while not user_exit:
            if system_input: print("Currently loaded: ")
            for element in system_input:
                print("- " + element)

            print("New element: respect type, 'q' to validate to launch")
            try:
                input_name: str = listing_input("- Name (str): ", str)
                input_mass: int = listing_input("- Mass (int): ", int)
                input_position_x: float = listing_input("- Starting position (x): ", float)
                input_position_y: float = listing_input("- Starting position (y): ", float)
                input_velocity_x: float = listing_input("- Starting velocity (x): ", float)
                input_velocity_y: float = listing_input("- Starting velocity (y): ", float)

                system_input[input_name] = settings.InputElement(
                    input_mass, 
                    Vector2D(input_position_x, input_position_y), 
                    input_name, 
                    input_mass // 100, 
                    Vector2D(input_velocity_x, input_velocity_y),
                )
                
            except ValueError as exception:
                if str(exception) == 'Exit':
                    user_exit = True
                    print("Choice validated.")
                else:
                    print("(!) app.ui.app_cmd() Value error; input anew.\n")

            except Exception as exception:
                print(f"(?) app.ui.app_cmd() Something else went wrong ({exception}). Retry.\n")

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
