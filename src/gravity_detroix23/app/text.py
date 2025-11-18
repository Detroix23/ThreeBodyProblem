"""
# Gravity.
src/gravity_detroix23/app/text.py  
"""
import pyxel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gravity_detroix23.app import game


class Text:
    """
    Text in app.
    """
    app: 'game.App'
    draw_main: bool
    texts_main: list[str]

    def __init__(self, app: 'game.App', draw_main: bool) -> None:
        self.app = app
        self.draw_main = draw_main
        self.texts_main = []

    def text_main(self, text_color: int = 8) -> None:
        """
        Draw main text.
        """
        x: int = int(self.app.simulation.camera.position.x) + 10
        y: int = int(self.app.simulation.camera.position.y) + 10
        for txt in self.texts_main:
            pyxel.text(x, y, txt, text_color)
            y += 6
    
    def draw(self) -> None:
        """
        Draw all text.
        """
        if self.draw_main:
            self.text_main()

    def update(self, text: list[str]) -> None:
        """
        Update the text body from given `text`.
        """
        self.texts_main = text
