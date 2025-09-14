from __future__ import annotations
import pyxel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import modules.app as app

class Text:
    """
    Text in app.
    """
    def __init__(self, app: app.App, draw_main: bool) -> None:
        self.APP: app.App = app
        self.draw_main: bool = draw_main

        self.texts_main: list[str] = []

    def text_main(self, text_color: int = 8) -> None:
        x: float = self.APP.simulation.camera.position.x + 10.0
        y: float = self.APP.simulation.camera.position.y + 10.0
        for txt in self.texts_main:
            pyxel.text(x, y, txt, text_color)
            y += 6
    
    def draw(self):
        if self.draw_main:
            self.text_main()

    def update(self, text_main: list[str]):
        self.texts_main = text_main