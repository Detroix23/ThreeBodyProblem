"""
THREE BODY PROBLEM
User configs
"""

import main


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

def app_cmd() -> None:
    """
    Basic starting sequence for the user, in CMD.
    """
    print("# Three body problem simulations")
    ## Config
    user_mode: str = input("Please select a mode {rand/conf/default}[default]: ")
    system_input: dict[str, tuple[int, tuple[int, int], str, int, tuple[float, float]]] = {}


    if user_mode not in ["", "rand", "conf", "default"]:
        user_mode = "default"
        print("(!) - Incorrect input; set to 'default'")
        

    if user_mode == "rand":
        print("# Mode selected: rand (random generation)")
        number_elements: int = main.random.randint(3, 5)
        i: int = 1
        while i <= number_elements:
            name_random: str = "Plan" + str(i)
            mass_random: int = main.random.randint(200, 800)
            position_x_random = main.random.randint(400, 600)
            position_y_random = main.random.randint(400, 600)
            system_input[name_random] = (mass_random, (position_x_random, position_y_random), name_random, int(mass_random / 100), (0, 0))
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

                system_input[manual['name']] = (
                    int(manual['mass']), (int(manual['position_x']), int(manual['position_y'])), manual['name'], int(int(manual['mass']) / 100), (0, 0)
                )
            except ValueError as E:
                if E.__str__() == 'Exit':
                    user_exit = True
                    print("Choice validated.")
                else:
                    print("(!) - Value error; input anew.\n")

            except Exception as E:
                print(f"(?) - Something else went wrong ({str(E)}). Enter anew element.\n")

    else:
        if not user_mode:
            print("# Mode selected: [default] (use default value)")
        else:
            print("# Mode selected: default (use default value)")

        system_input["Plan1"] = (10500, (445, 560), "Plan1", 15, (10, 0))
        system_input["Plan2"] = (400, (580, 450), "Plan2", 4, (0, 10))
        system_input["Plan3"] = (300, (400, 400), "Plan3", 3, (0, 10))
        system_input["Plan4"] = (300, (300, 350), "Plan4", 3, (0, 10))

    # Warnings (!)
    if not system_input:
        print("# (!) - Empty system.")
    elif len(system_input) == 1:
        print("# (!) - One element system.")

    print("Starting...")

    # Completion
    SIM: main.Board = main.Board(
        width=1000, height=1000, title="Simulation", fps=30, edges="none", 
        system=system_input, mass_softener=1, gravitational_constant=(6.67*(10**1)),
        exponent_softener=-0.0, bounce_factor=1.0
    )
    

if __name__ == "__main__":
    print("THREE BODY PROBLEM - Libraries.")
    print("UI.")