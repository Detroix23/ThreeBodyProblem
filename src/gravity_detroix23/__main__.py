"""
THREE BODY PROBLEM
Simulation of planet movement
Use of gravitational formula: F = (m1*m2) / d**2
We consider that all elements are spherical
Run: 1st
"""
import sys

from gravity_detroix23.modules import settings
from gravity_detroix23.app import (
	game,
	ui,
)
from gravity_detroix23.modules import (
    writter,
    defaults,
    console,
)


def main(args: list[str]) -> None:
    print("# Gravity.")

    if "--help" in args:
        print(console.HELP_STRING)
        return

    print("*Starting...*\n")

    system: dict[str, settings.InputElem] = ui.app_cmd()
    system_string: dict[str, str] = {elem_name: elem_info.__str__() for elem_name, elem_info in system.items()}
    
    writter.board_settings(
        system = writter.system(system_string),
        board_settings = ",".join([f"{name}={value}" for name, value in defaults.app_dict().items()])
    )
    
    game.App(
        system=system, 
        width=defaults.APP.BOARD_WIDTH,      
        height=defaults.APP.BOARD_HEIGHT, 
        title=defaults.APP.TITLE, 
        fps=defaults.APP.FPS,
        gravitational_constant=defaults.APP.G,
        edges=defaults.APP.EDGE,
        bounce_factor=defaults.APP.BOUNCE_FACTOR,
        mass_softener=defaults.APP.MASS_SOFTENER, 
        exponent_softener=defaults.APP.EXPONENENT_SOFTENER,
        collisions=defaults.APP.COLLISIONS,
        grid_draw_vector=defaults.APP.GRID_DRAW_VECTORS,
        draw_velocity=defaults.APP.DRAW_VELOCITY, 
        draw_force=defaults.APP.DRAW_FORCE, 
        draw_text=defaults.APP.DRAW_TEXT,
        draw_grid=defaults.APP.DRAW_GRID,
    )

    print("---\nEnd")

main(sys.argv)
