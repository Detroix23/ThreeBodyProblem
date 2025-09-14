"""
THREE BODY PROBLEM
Simulation of planet movement
Use of gravitational formula: F = (m1*m2) / d**2
We consider that all elements are spherical
Run: 1st
"""

# Imports
# Local
import modules.settings as settings
import modules.app as app
import modules.ui as ui
import modules.writter as writter

TITLE: str = "Simulation"
BOARD_WIDTH: int  = 1000
BOARD_HEIGHT: int = 1000
FPS: int = 25

G: float = (6.67*(10**2))
EDGE: settings.Edge = settings.Edge.NONE
BOUNCE_FACTOR: float = 1.0
MASS_SOFTENER: float = 1.0
EXPONENENT_SOFTENER: float = -0.0
DRAW_VELOCITY: bool = True
DRAW_FORCE: bool = False
DRAW_TEXT: bool = True
DRAW_GRID: bool = True
COLLISIONS: settings.CollisionsBehaviour = settings.CollisionsBehaviour.COLLIDE_WITH_FUSION
GRID_DRAW_VECTORS: bool = False
DEFAULT_MODE: settings.SimMode = settings.SimMode.DEFAULT 

def main() -> None:
    system: dict[str, settings.InputElem] = ui.app_cmd()
    system_string: dict[str, str] = {elem_name: elem_info.__str__() for elem_name, elem_info in system.items()}
    print(f"! Using system={system_string}. Logging...")
    writter.board_settings(
        system = writter.system(system_string),
        board_settings = f"edges={EDGE}, bounce={BOUNCE_FACTOR}, mass_softener={MASS_SOFTENER}, exponenent_softener={EXPONENENT_SOFTENER}, draw_velocity={DRAW_VELOCITY}, draw_force={DRAW_FORCE}, draw_text={DRAW_TEXT}, draw_grid={DRAW_GRID}, collisions={COLLISIONS}"
    )
    
    APP: app.App = app.App(
        system = system, 
        width = BOARD_WIDTH, 
        height = BOARD_HEIGHT, 
        title = TITLE, 
        fps = FPS,
        gravitational_constant = G,
        edges = EDGE,
        bounce_factor = BOUNCE_FACTOR,
        mass_softener = MASS_SOFTENER, 
        exponent_softener = EXPONENENT_SOFTENER,
        collisions=COLLISIONS,
        grid_draw_vector=GRID_DRAW_VECTORS,
        draw_velocity = DRAW_VELOCITY, 
        draw_force = DRAW_FORCE, 
        draw_text = DRAW_TEXT,
        draw_grid = DRAW_GRID
    )

    print("---\nEnd")


if __name__ == "__main__":
    main()

