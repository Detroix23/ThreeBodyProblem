"""
# Three Body Problem.
src/gravity_detroix23/__main__.py  

Simulation of planet movement. 
Use of gravitational formula: F = (m1*m2) / d^2
We consider that all elements are spherical
"""
import sys

try:
    import gravity_detroix23   # pyright: ignore[reportUnusedImport]

except ModuleNotFoundError as module_not_found:
    print("(X) __main__ Missing module `gravity_detroix23`.")
    print(f"Full output: ```\n{module_not_found}\n```")
    print("""(?) __main__ Try installing this code locally, in virtual environment: 
```shell
python -m venv .venv

# Windows.
./.venv/Scripts/activate
# Unix.
source ./.venv/bin/activate
          
python -m pip install .   
```   
""")

from gravity_detroix23.inputs import ui
from gravity_detroix23.modules import settings, writer, defaults, console
from gravity_detroix23.app import app


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
            for name, value in defaults.App.to_dict().items()
        ])
    )
    
    gravity = app.App(
        system, 
        defaults.App.width,
        defaults.App.height,
        defaults.App.title,
        defaults.App.fps,
        defaults.App.gravitational_constant,
        defaults.App.edges,
        defaults.App.bounce_factor,
        defaults.App.mass_softener,
        defaults.App.exponent_softener,
        settings.CollisionsBehavior.COLLIDE,
        defaults.App.grid_draw_vector,
        draw_velocity=True,
        draw_force=True,
        draw_text=defaults.App.draw_text,
        draw_grid=defaults.App.draw_grid,
    )
    
    gravity.run()

    print("---\nEnd")

main(sys.argv)
