
import modules.settings
import ui
import simulation
import text
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
        grid_draw_vector: bool,
        draw_velocity: bool = True, 
        draw_force: bool = True, 
        draw_text: bool = True, 
        draw_grid: bool = True,
    ) -> None:
        # Simulation
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
        # Text
        self.text: text.Text = text.Text(
            app=self,
            draw_main=True
        )
        """
        [
            f"# Three Body Problem - title={title}; edges={edges}, fps={str(fps)}, frames={str(frame_count)}",
            f"- Controls: zoom={str(zoom)}, camera: x={str(camera.x)}; y={str(camera.y)}",
            f"- Time: speed={str(time_speed)}, fpf={frame_per_frame}",
            f"- Elements: total={str(len(system))}",
            "---"
        ]
        """

        # Simulation screen
        pyxel.init(width, height, title=title, fps=fps)
        print("- Pyxel initialized")
        # Ressource file
        pyxel.load(modules.settings.RESSOURCE_FILE)
        # Run
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        self.simulation.update()
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