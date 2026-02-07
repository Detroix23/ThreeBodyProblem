"""
# Gravity.
gravity/src/modules/types.py  
"""

import typing

import gravity_detroix23.modules.settings as settings

pretty_supported = typing.Union[dict[typing.Any, typing.Any], list[typing.Any]] 
setting = typing.Union[str, int, float, bool, settings.Edge, settings.CollisionsBehavior, settings.SimMode]
Number = typing.Union[float, int]

def is_pretty_supported(argument: typing.Any) -> bool:
	"""
	Check if the argument is in the `pretty_supported` `Union`.
	"""
	types: list[type] = []
	for t in typing.get_args(pretty_supported):
		if typing.get_origin(t):
			types.append(typing.get_origin(t))
		else:
			types.append(t)

	return any(isinstance(argument, t) for t in types)
