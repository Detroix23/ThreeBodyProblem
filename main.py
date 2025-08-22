"""
THREE BODY PROBLEM
Simulation of planet movement
Use of gravitational formula: F = (m1*m2) / d**2
We consider that all elements are spherical
Run: 1st
"""

# Imports
# Local
import modules.settings
import app

TITLE: str = "Simulation"
BOARD_WIDTH: int  = 1000
BOARD_HEIGHT: int = 1000
FPS: int = 25

G: float = (6.67*(10**2))
EDGE: modules.settings.Edge = modules.settings.Edge.NONE
BOUNCE_FACTOR: float = 1.0
MASS_SOFTENER: float = 1.0
EXPONENENT_SOFTENER: float = -0.0
DRAW_VELOCITY: bool = True
DRAW_FORCE: bool = False
DRAW_TEXT: bool = True
DRAW_GRID: bool = True
COLLISIONS: modules.settings.CollisionsBehaviour = modules.settings.CollisionsBehaviour.COLLIDE_WITH_FUSION

DEFAULT_MODE: modules.settings.SimMode = modules.settings.SimMode.DEFAULT 

import ui
import modules.writter


# Run 1st.
if __name__ == "__main__":
    
    system: dict[str, ui.InputElem] = ui.app_cmd()
    
    system_string: dict[str, str] = {elem_name: elem_info.__str__() for elem_name, elem_info in system.items()}
    print(f"! Using system={system_string}. Logging...")
    modules.writter.board_settings(
        system = modules.writter.system(system_string),
        board_settings = f"edges={EDGE}, bounce={BOUNCE_FACTOR}, mass_softener={MASS_SOFTENER}, exponenent_softener={EXPONENENT_SOFTENER}, draw_velocity={DRAW_VELOCITY}, draw_force={DRAW_FORCE}, draw_text={DRAW_TEXT}, draw_grid={DRAW_GRID}, collisions={COLLISIONS}"
    )
    
    SIM: app.App = app.App(
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
        draw_velocity = DRAW_VELOCITY, 
        draw_force = DRAW_FORCE, 
        draw_text = DRAW_TEXT,
        draw_grid = DRAW_GRID
    )
    
    
    print("---\nEnd")




