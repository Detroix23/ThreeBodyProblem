"""
THREE BODY PROBLEM
User configs
"""
import random

from maths_local import *
import main

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
        


def app_cmd() -> None:
    """
    Basic starting sequence for the user, in CMD.
    """
    print("# Three body problem simulations")
    ## Config
    user_mode: str = input("Please select a mode {rand/conf/default}[default]: ")
    system_input: dict[str, InputElem] = {}


    if user_mode not in ["", "rand", "conf", "default"]:
        user_mode = "default"
        print("(!) - Incorrect input; set to 'default'")
        

    if user_mode == "rand":
        print("# Mode selected: rand (random generation)")
        number_elements: int = random.randint(3, 5)
        i: int = 1
        while i <= number_elements:
            name_random: str = "Plan" + str(i)
            mass_random: int = random.randint(200, 800)
            position_x_random = random.randint(400, 600)
            position_y_random = random.randint(400, 600)
            system_input[name_random] = InputElem(mass_random, Vector2D(position_x_random, position_y_random), name_random, int(mass_random / 100), Vector2D(0, 0))
            i += 1

    elif user_mode == "conf":
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
        if not user_mode:
            print("# Mode selected: [default] (use default value)")
        else:
            print("# Mode selected: default (use default value)")

        system_input["Plan1"] = InputElem(10500, Vector2D(445, 560), "Plan1", 15, Vector2D(0, 0))
        system_input["Plan2"] = InputElem(400, Vector2D(580, 450), "Plan2", 4, Vector2D(0, 10))
        system_input["Plan3"] = InputElem(300, Vector2D(400, 400), "Plan3", 3, Vector2D(0, 10))
        system_input["Plan4"] = InputElem(300, Vector2D(300, 350), "Plan4", 3, Vector2D(0, 10))

    # Warnings (!)
    if not system_input:
        print("# (!) - Empty system.")
    elif len(system_input) == 1:
        print("# (!) - One element system.")

    print("Starting...")

    # Completion
    SIM: main.Board = main.Board(
        system=system_input, width=1000, height=1000, title="Simulation", fps=25,
        gravitational_constant=(6.67*(10**2)),
        edges="none", bounce_factor=1.0,
        mass_softener=1, exponent_softener=-0.0,
        draw_velocity=True, draw_force=True, draw_text=True
    )
    print(f"! Used SIM={SIM}")

if __name__ == "__main__":
    print("THREE BODY PROBLEM - Libraries.")
    print("UI.")