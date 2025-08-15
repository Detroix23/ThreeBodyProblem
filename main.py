"""
THREE BODY PROBLEM
Simulation of planet movement
Use of gravitational formula: F = (m1*m2) / d**2
We consider that all elements are spherical
Run: 1st
"""

# Imports
# Local
import simulation

BOARD_WIDTH: int  = 1000
BOARD_HEIGHT: int = 1000

import ui


        
        

# Simulation


# Run 1st.
if __name__ == "__main__":
    
    SIM: simulation.Board = simulation.Board(
        system=ui.app_cmd(), 
        width=BOARD_WIDTH, 
        height=BOARD_HEIGHT, 
        title="Simulation", 
        fps=25,
        gravitational_constant=(6.67*(10**2)),
        edges="none", 
        bounce_factor=1.0,
        mass_softener=1, 
        exponent_softener=-0.0,
        draw_velocity=True, 
        draw_force=False, 
        draw_text=True,
        draw_grid=True
    )
    print(f"! Used SIM={SIM}")

    print("---\nEnd")




