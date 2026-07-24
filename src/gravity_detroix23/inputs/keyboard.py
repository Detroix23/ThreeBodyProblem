"""
# Gravity.  
src/gravity_detroix23/inputs/keyboard.py  
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from gravity_detroix23.app.board import Board
from gravity_detroix23.modules import scene_objects, keys

class Buttons(scene_objects.Updatable):
    """
    Manage user presses.  
    Uses mainly `pyxel.btn` method.   
    """
    board: 'Board'
    key_sensitives: list[keys.KeySensitive]

    def __init__(self, board: 'Board') -> None:
        self.board = board
        self.key_sensitives: list[keys.KeySensitive] = [
            self.board.times,
            self.board.camera,
        ]

        print("\n## Usage: ")
        print(self.describe_binding(), end="\n---\n\n")

        return

    def describe_binding(self) -> str:
        """
        Returns a formatted help string describing all registered bindings.
        """
        return "- " + ("\n- ".join([
            f"{keys.PYXEL_KEYS[binding.key_code]}: {binding.description}"
            for sensitive in self.key_sensitives
            for binding in sensitive.get_bindings()
        ]))

    def update(self) -> None:
        """
        Listen to user inputs
        """
        for sensitive in self.key_sensitives:
            keys.apply_bindings(sensitive.get_bindings())

        return
