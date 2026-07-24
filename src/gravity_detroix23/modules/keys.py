"""
# Gravity.
gravity/src/modules/keys.py  
"""
import abc
import enum
from typing import Callable

import pyxel


class Trigger(enum.Enum):
    """
    # Enumerate way to `Trigger` key detection.
    """
    ALL = 0
    """ Calls `pyxel.btn`.  """
    PRESSED = 1
    """ Calls `pyxel.btnp`. """
    RELEASED = 2
    """ Calls `pyxel.btnr`. """


class KeyBinding:
    """
    # Description of a `KeyBinding`.
    """
    key_code: int
    description: str
    function: Callable[[], None]
    trigger: Trigger

    def __init__(
        self,
        key_code: int,
        description: str,
        function: Callable[[], None],
        trigger: Trigger = Trigger.ALL,
    ) -> None:
        assert key_code >= 0
        self.key_code = key_code
        assert description
        self.description = description
        self.function = function
        self.trigger = trigger
        
        return

    def __repr__(self) -> str:
        return (
            f"KeyBinding(key_code={self.key_code}, description={self.description} "
            f"function={self.function}, trigger={self.trigger})"
        )


class KeySensitive(metaclass=abc.ABCMeta):
    """
    # All `KeySensitive` objects that should react to user key input.
    """
    @abc.abstractmethod
    def get_bindings(self) -> list[KeyBinding]:
        """
        Returns the `list` of bindings: (`int` key code; `str` description).
        """
        ...

def apply_bindings(bindings: list[KeyBinding]) -> None:
    """
    Iterates `target`'s bindings and apply them if called.
    """
    for binding in bindings:
        if (
            (   
                binding.trigger is Trigger.PRESSED
                and pyxel.btnp(binding.key_code)
            )
            or (
                binding.trigger is Trigger.RELEASED
                and pyxel.btnr(binding.key_code)
            ) or (
                binding.trigger is Trigger.ALL
                and pyxel.btn(binding.key_code)
            )
        ):
            binding.function()
        
    return
