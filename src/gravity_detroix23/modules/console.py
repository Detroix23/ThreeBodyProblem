"""
# Gravity.
src/gravity/modules/console.py  
"""
from gravity_detroix23.modules import types

HELP_STRING: str = """## Help.

Console.
 --help: Show this message.
    
GUI, key press.
 {1, 2, 3, 4, 5, 6}: Set time speed (1 normal, 6 slowest).
 Space: Pause/ Unpause time.  
 Arrows: Move camera.
 Page Up: Zoom in (W.I.P.).
 Page Down: Zoom out (W.I.P.).
 Home: Reset camera.
 G: Enable/ Disable grid.
 E: Enable/ Disable drawing elements.
 R: Enable/ Disable drawing force vectors.
 F: Enable/ Disable drawing velocity vectors.
 T: Enable/ Disable all text.
 Y: Enable/ Disable drawing trails.

More info:
 cf. README.md
"""

def pretty(
    element: types.pretty_supported, 
    recursive: bool = True,
    tab: str = "  ",
    end: str = "\n",
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
                display.append(f"{tab * depth}{name}: {value_pretty}, ")      
            else:    
                display.append(f"{tab * depth}{name}: {value}, ")

        display.append(tab * (depth - 1) + "}" + end)

    else:
        display.append("[")
        for value in element:
            if recursive and types.is_pretty_supported(value):
                display.append(f"{tab * depth}{pretty(value)}, ")      
            else:    
                display.append(f"{tab * depth}{value}, ")

        display.append(tab * (depth - 1) + "]" + end)

    return "\n".join(display)



