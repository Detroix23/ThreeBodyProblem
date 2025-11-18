"""
THREE BODY PROBLEM.
Logging and writting.
"""
import datetime

from gravity_detroix23.modules import paths

def system(system: dict[str, str]) -> str:
    string: str = ""
    for _, elem in system.items():
        string += f"\t{elem};\n"    
    return string

def board_settings(system: str, board_settings: str) -> None:
    """
    Take the board settings, preformatted as a string, and write the logs. 
    """
    # Project path.
    try:
        with open(paths.LOGS, "a") as logs:
            logs.write(f"Simulation: {datetime.datetime.now()};\n")
            logs.write(f"System:\n{system}")
            logs.write(f"Settings: {board_settings}\n")
            logs.write("\n")
    except OSError:
        print(f"(!) - Directory not found `{paths.LOGS}`.")
