"""
# Gravity.
gravity/src/modules/entity.py  
"""
import abc

from gravity_detroix23.modules.scene_objects import SceneObject
from gravity_detroix23.physics.vectors import Vector2D

class Entity(SceneObject, metaclass=abc.ABCMeta):
    """
    # Trait for all "real" `Entity` and physical objects.
    """

    def get_id(self) -> int:
        """
        Returns the unique ID of the `Entity`.
        """
        ...

    def get_position(self) -> Vector2D:
        """
        Returns the position of the `Entity`.
        """
        ...

    def get_velocity(self) -> Vector2D:
        """
        Returns the velocity of the `Entity`.
        """
        ...

    def get_acceleration(self) -> Vector2D:
        """
        Returns the acceleration of the `Entity`.
        """
        ...

    def set_position(self, vector: Vector2D) -> None:
        """
        Set the position of the `Entity` to `vector`.
        """
        ...

    def set_velocity(self, vector: Vector2D) -> None:
        """
        Set the velocity of the `Entity` to `vector`.
        """
        ...

    def set_acceleration(self, vector: Vector2D) -> None:
        """
        Set the acceleration of the `Entity` to `vector`.
        """
        ...
    