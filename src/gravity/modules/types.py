"""
# Gravity.
gravity/src/modules/types.py  
"""

import typing

import modules.settings as settings

setting = typing.Union[str, int, float, bool, settings.Edge, settings.CollisionsBehaviour, settings.SimMode]
