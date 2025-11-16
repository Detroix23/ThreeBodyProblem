"""
# Gravity.
src/gravity/app/game.py  
Load and generate a `pyxel` game.
"""

import pyxel

from gravity.modules import (
	settings, 
	paths, 
	text
)
from gravity.app import simulation



class App:
    """
    # App.
    Contains and intialize the pyxel runtime.
    """
    simulation: simulation.Board
    text: text.Text

    def __init__(
        self, 
        system: dict[str, settings.InputElem], 
        width: int, 
        height: int, 
        title: str, 
        fps: int, 
        gravitational_constant: float, 
        edges: settings.Edge, 
        bounce_factor: float,  
        mass_softener: float, 
        exponent_softener: float,
        collisions: settings.CollisionsBehaviour, 
        grid_draw_vector: bool,
        draw_velocity: bool = True, 
        draw_force: bool = True, 
        draw_text: bool = True, 
        draw_grid: bool = True,
    ) -> None:
        # Simulation.
        self.simulation: simulation.Board = simulation.Board(
            system,
            width,
            height,
            title,
            fps,
            gravitational_constant,
            edges,
            bounce_factor,
            mass_softener,
            exponent_softener,
            collisions,
            grid_draw_vector,
            draw_velocity,
            draw_force,
            draw_text,
            draw_grid
        )
        # Text.
        self.text: text.Text = text.Text(
            app=self,
            draw_main=True
        )

        # Simulation screen.
        pyxel.init(width, height, title=title, fps=fps)
        print("- Pyxel initialized")
        # Ressource file.
        try:
            pyxel.load(str(paths.RESSOURCE_FILE))
        except Exception as exception:
            raise Exception(f"(X) - Couldn't open ressource file in {paths.RESSOURCE_FILE}. {type(exception).__name__}: `{exception.args}`.")

        # Run.
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        # Gravity.
        self.simulation.update()
        # Text.
        self.text.update(
            text_main=[
                f"# Three Body Problem - title={self.simulation.title}; edges={self.simulation.edges}, fps={str(self.simulation.fps)}, frames={str(pyxel.frame_count)}",
                f"- Controls: zoom={str(self.simulation.zoom)}, camera: x={str(self.simulation.camera.x)}; y={str(self.simulation.camera.y)}",
                f"- Time: speed={str(self.simulation.time_speed)}, fpf={self.simulation.frame_per_frame}",
                f"- Elements: total={str(len(self.simulation.system))}",
                "---"
            ]
        )
    
    def draw(self) -> None:
        self.simulation.draw()
        self.text.draw()
