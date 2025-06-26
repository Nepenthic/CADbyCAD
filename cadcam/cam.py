from .model import Profile


def generate_gcode(
    profile: Profile,
    depth: float = 1.0,
    feedrate: float = 1000.0,
    passes: int = 1,
) -> str:
    """Generate simple contour G-code with optional multiple passes."""
    lines = [
        "G21 ; set units to millimeters",
        f"G1 F{feedrate}"
    ]
    pass_depth = depth / max(1, passes)
    for p in range(passes):
        z = -(p + 1) * pass_depth
        lines.append(f"; pass {p + 1}")
        for x, y in profile.points:
            lines.append(f"G1 X{x:.3f} Y{y:.3f} Z{z:.3f}")
        lines.append("G1 Z0.000")
    lines.append("M2")
    return "\n".join(lines)
