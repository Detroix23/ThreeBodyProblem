"""
THREE BODY PROBLEM.
Logging and writting.
"""

import datetime

def system(system: dict[str, str]) -> str:
    string: str = ""
    for _, elem in system.items():
        string += f"\t{elem};\n"    
    return string

def board_settings(system: str, board_settings: str) -> None:
    """
    Take the board settings, preformatted as a string, and write the logs. 
    """
    logs_path: str = "..\\logs\\main.log"
    with open(logs_path, "a") as logs:
        logs.write(f"Simulation: {datetime.datetime.now()};\n")
        logs.write(f"System:\n{system}")
        logs.write(f"Settings: {board_settings}\n")
        logs.write("\n")
