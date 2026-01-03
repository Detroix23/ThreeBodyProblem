"""
# Gravity.
src/gravity/app/game.py  
Load and generate a `pyxel` game.
"""

import time
import pyxel

from gravity_detroix23.modules import (
	settings, 
	paths
)
from gravity_detroix23.app import (
	board, 
	text,
)
from gravity_detroix23.inputs import mouse



class App:
    """
    # App.
    Contains all the simulation, parallel workers, and initialize the pyxel runtime.
    """
    simulation: board.Board
    text: text.Text
    mouse: mouse.Mouse

    _time_update: float
    _time_draw: float

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
        collisions: settings.CollisionsBehavior, 
        grid_draw_vector: bool,
        draw_velocity: bool = True, 
        draw_force: bool = True, 
        draw_text: bool = True, 
        draw_grid: bool = True,
    ) -> None:
        # Workers
        self.simulation: board.Board = board.Board(
            self,
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
        
        self.text: text.Text = text.Text(self, draw_main=True)
        self.mouse: mouse.Mouse = mouse.Mouse(self, 2)

        self._time_draw = 0.0
        self._time_update = 0.0

        # Simulation screen.
        pyxel.init(width, height, title=title, fps=fps)
        print("- Pyxel initialized")
        # Resource file.
        try:
            pyxel.load(str(paths.RESOURCE_FILE))
        except Exception as exception:
            raise Exception(f"(X) - Couldn't open resource file in {paths.RESOURCE_FILE}. {type(exception).__name__}: `{exception.args}`.")

        # Run.
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        """
        Update everything.
        """
        self._time_update = time.perf_counter() - self._time_update

        self.simulation.update()
        self.mouse.listen()
        # Text.
        self.text.update([
            f"# Three Body Problem - title={self.simulation.title}; edges={self.simulation.edges}, fps={str(self.simulation.fps)}, frames={str(pyxel.frame_count)}",
            f"= Frames: draw={self._time_draw}s, update={self._time_update}s",
            f"- Controls: zoom={str(self.simulation.camera.zoom)}, camera: x={str(self.simulation.camera.position.x)}; y={str(self.simulation.camera.position.y)}",
            f"- Time: speed={str(self.simulation.times.speed)}, fpf={self.simulation.times.frame_per_frame}",
            f"- Elements: total={str(len(self.simulation.system))}",
            "---"
        ])
    
        self._time_update = time.perf_counter()

    def draw(self) -> None:
        """
        Draw everything.
        """
        self._time_draw = time.perf_counter()
        
        self.simulation.draw()
        self.text.draw()
        self.mouse.draw()

        self._time_draw = time.perf_counter() - self._time_draw