"""
# Gravity.
src/gravity_detroix23/app/text.py  
"""
import pyxel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gravity_detroix23.app.app import App
from gravity_detroix23.modules import scene_objects

class Text(scene_objects.Drawable):
    """
    # `Text` in app.
    """
    app: 'App'
    draw_main: bool
    texts_main: list[str]
    line_spacing: int
    color: int

    def __init__(
        self, 
        app: 'App', 
        draw_main: bool,
        line_spacing: int = 6,
        color: int = 8
    ) -> None:
        self.app = app
        self.draw_main = draw_main
        self.texts_main = []
        self.line_spacing = line_spacing
        self.color = color

        return
    
    def draw(self) -> None:
        """
        Draw all text.

        Text is on top of the camera, fixed.
        """
        if self.draw_main:
            x: int = 10
            y: int = 10
            for text in self.texts_main:
                pyxel.text(x, y, text, self.color)
                y += self.line_spacing

        return

    def update_text(self, text: list[str]) -> None:
        """
        Update the text body from given `text`.
        """
        self.texts_main = text

        return
    