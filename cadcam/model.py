from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Profile:
    """Simple 2D profile represented by a list of (x, y) coordinates."""
    points: List[Tuple[float, float]]

    @staticmethod
    def from_csv(path: str) -> "Profile":
        """Load a profile from a CSV file with rows of 'x,y'."""
        pts = []
        with open(path, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                x_str, y_str = line.strip().split(',')
                pts.append((float(x_str), float(y_str)))
        return Profile(pts)

@dataclass
class Extrusion:
    """Extruded 3D shape from a 2D profile."""
    profile: Profile
    height: float

    def to_stl(self) -> str:
        """Generate an ASCII STL string for the extrusion."""
        from math import sqrt

        def fmt_pt(p):
            return f"{p[0]:.6f} {p[1]:.6f} {p[2]:.6f}"

        def normal(p1, p2, p3):
            ux, uy, uz = p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2]
            vx, vy, vz = p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2]
            nx, ny, nz = (
                uy*vz - uz*vy,
                uz*vx - ux*vz,
                ux*vy - uy*vx
            )
            length = sqrt(nx*nx + ny*ny + nz*nz) or 1.0
            return nx/length, ny/length, nz/length

        pts2d = self.profile.points
        top = [(x, y, self.height) for x, y in pts2d]
        bottom = [(x, y, 0.0) for x, y in pts2d]
        n = len(pts2d)
        lines = ["solid extrusion"]
        # sides
        for i in range(n):
            j = (i + 1) % n
            p1, p2, p3, p4 = bottom[i], bottom[j], top[j], top[i]
            for tri in ((p1, p2, p3), (p1, p3, p4)):
                nx, ny, nz = normal(*tri)
                lines.append(f"facet normal {nx:.6f} {ny:.6f} {nz:.6f}")
                lines.append("  outer loop")
                for p in tri:
                    lines.append(f"    vertex {fmt_pt(p)}")
                lines.append("  endloop")
                lines.append("endfacet")
        # bottom
        for i in range(1, n-1):
            tri = (bottom[0], bottom[i+1], bottom[i])
            nx, ny, nz = normal(*tri)
            lines.append(f"facet normal {nx:.6f} {ny:.6f} {nz:.6f}")
            lines.append("  outer loop")
            for p in tri:
                lines.append(f"    vertex {fmt_pt(p)}")
            lines.append("  endloop")
            lines.append("endfacet")
        # top
        for i in range(1, n-1):
            tri = (top[0], top[i], top[i+1])
            nx, ny, nz = normal(*tri)
            lines.append(f"facet normal {nx:.6f} {ny:.6f} {nz:.6f}")
            lines.append("  outer loop")
            for p in tri:
                lines.append(f"    vertex {fmt_pt(p)}")
            lines.append("  endloop")
            lines.append("endfacet")
        lines.append("endsolid extrusion")
        return "\n".join(lines)
