from typing import Iterable
from .model import Profile


def generate_gcode(profile: Profile, depth: float = 1.0, feedrate: float = 1000.0) -> str:
    """Generate very simple G-code for tracing the profile."""
    lines = [
        "G21 ; set units to millimeters",
        f"G1 F{feedrate}"
    ]
    for x, y in profile.points:
        lines.append(f"G1 X{x:.3f} Y{y:.3f} Z0.000")
        lines.append(f"G1 Z{-depth:.3f}")
        lines.append("G1 Z0.000")
    lines.append("M2")
    return "\n".join(lines)
