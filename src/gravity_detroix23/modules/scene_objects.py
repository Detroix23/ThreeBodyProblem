"""
# Gravity.
gravity/src/modules/scene_objects.py  
"""
import abc

class Updatable(metaclass=abc.ABCMeta):
    """
    # Generic trait for all `Updatable` objets.
    """
    @abc.abstractmethod
    def update(self) -> None:
        """
        Update the objet and its children.
        """
        ...


class Drawable(metaclass=abc.ABCMeta):
    """
    # Generic trait for all `Drawable` objets.
    """
    @abc.abstractmethod
    def draw(self) -> None:
        """
        Draw the objet and its children.
        """
        ...


class SceneObject(Updatable, Drawable, metaclass=abc.ABCMeta):
    """
    # All `SceneObject`s that are `Updatable` and `Drawable`.
    """
