import pyxel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gravity_detroix23.app import game


class Text:
    """
    Text in app.
    """
    def __init__(self, app: 'game.App', draw_main: bool) -> None:
        self.APP = app
        self.draw_main: bool = draw_main

        self.texts_main: list[str] = []

    def text_main(self, text_color: int = 8) -> None:
        x: int = int(self.APP.simulation.camera.x) + 10
        y: int = int(self.APP.simulation.camera.y) + 10
        for txt in self.texts_main:
            pyxel.text(x, y, txt, text_color)
            y += 6
    
    def draw(self):
        if self.draw_main:
            self.text_main()

    def update(self, text_main: list[str]):
        self.texts_main = text_main
