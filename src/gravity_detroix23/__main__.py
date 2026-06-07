"""
# Three Body Problem.
src/gravity_detroix23/__main__.py  

Simulation of planet movement. 
Use of gravitational formula: F = (m1*m2) / d**2
We consider that all elements are spherical
"""
import sys

try:
    import gravity_detroix23   # pyright: ignore[reportUnusedImport]

except ModuleNotFoundError as module_not_found:
    print("(X) Missing module `gravity_detroix23`.")
    print(f"Full output: ```\n{module_not_found}\n```")
    print("""(?) Try installing this code locally, in virtual environment: 
    ```shell
    python -m venv .venv

    pip install .   
    ```   
""")

from gravity_detroix23.modules import settings, writer
from gravity_detroix23.app import app, ui
from gravity_detroix23.modules import defaults, console


def main(args: list[str]) -> None:
    """
    Three body problem entry point.
    """
    print("\n# Gravity.\n")

    if "--help" in args:
        print(console.HELP_STRING)
        return

    print("## Set up the universe.\n")

    system: dict[str, settings.InputElement] = ui.app_cmd()
    system_string: dict[str, str] = {
        name: str(info) 
        for name, info in system.items()
    }
    
    writer.board_settings(
        system = writer.system(system_string),
        board_settings = ",".join([
            f"{name}={value}" 
            for name, value in defaults.app_dict().items()
        ])
    )
    
    gravity = app.App(
        system=system, 
        width=defaults.APP.BOARD_WIDTH,      
        height=defaults.APP.BOARD_HEIGHT, 
        title=defaults.APP.TITLE, 
        fps=defaults.APP.FPS,
        gravitational_constant=defaults.APP.G,
        edges=defaults.APP.EDGE,
        bounce_factor=defaults.APP.BOUNCE_FACTOR,
        mass_softener=defaults.APP.MASS_SOFTENER, 
        exponent_softener=defaults.APP.EXPONENT_SOFTENER,
        collisions=defaults.APP.COLLISIONS,
        grid_draw_vector=defaults.APP.GRID_DRAW_VECTORS,
        draw_velocity=defaults.APP.DRAW_VELOCITY, 
        draw_force=defaults.APP.DRAW_FORCE, 
        draw_text=defaults.APP.DRAW_TEXT,
        draw_grid=defaults.APP.DRAW_GRID,
    )
    
    gravity.run()

    print("---\nEnd")

main(sys.argv)
