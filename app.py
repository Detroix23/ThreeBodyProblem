
import modules.settings
import ui
import simulation
import pyxel


class App:
    """
    Contains all the pyxel runtime.
    """
    def __init__(
        self, 
        system: dict[str, ui.InputElem], 
        width: int, 
        height: int, 
        title: str, 
        fps: int, 
        gravitational_constant: float, 
        edges: modules.settings.Edge, 
        bounce_factor: float,  
        mass_softener: float, 
        exponent_softener: float,
        collisions: modules.settings.CollisionsBehaviour, 
        draw_velocity: bool = True, 
        draw_force: bool = True, 
        draw_text: bool = True, 
        draw_grid: bool = True,
    ) -> None:
        # Init simulation
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
            draw_velocity,
            draw_force,
            draw_text,
            draw_grid
        )

        # Init simulation screen
        pyxel.init(width, height, title=title, fps=fps)
        print("- Pyxel initialized")
        # Ressource file
        pyxel.load(modules.settings.RESSOURCE_FILE)


        # Run
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        self.simulation.update()

    def draw(self) -> None:
        self.simulation.draw()