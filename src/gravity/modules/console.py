"""
# Gravity.
src/gravity/modules/console.py  
"""
from gravity.modules import types

def pretty(
    element: types.pretty_supported, 
    recursive: bool = True,
    tab: str = "  ",
    *,
    depth: int = 1,
) -> str:
    """
    Return a pretty formatted string for any valid type.
    """
    display: list[str] = []

    if isinstance(element, dict):
        display.append("{")
        for name, value in element.items():
            if recursive and types.is_pretty_supported(value):
                value_pretty: str = pretty(value, True, tab, depth=depth + 1)
                display.append(f"{tab * depth}{name}: {value_pretty}")      
            else:    
                display.append(f"{tab * depth}{name}: {value}")

        display.append(tab * (depth - 1) + "}\n")

    else:
        display.append("[")
        for value in element:
            if recursive and types.is_pretty_supported(value):
                display.append(f"{tab * depth}{pretty(value)}")      
            else:    
                display.append(f"{tab * depth}{value}")

        display.append(tab * (depth - 1) + "]\n")

    return "\n".join(display)
