from dataclasses import dataclass
from typing import List, Tuple, Optional

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

    # --- basic transforms ---
    def translated(self, dx: float, dy: float) -> "Profile":
        """Return a new profile translated by (dx, dy)."""
        return Profile([(x + dx, y + dy) for x, y in self.points])

    def scaled(self, sx: float, sy: Optional[float] = None) -> "Profile":
        """Return a new profile scaled relative to the origin."""
        sy = sy if sy is not None else sx
        return Profile([(x * sx, y * sy) for x, y in self.points])

    def rotated(self, angle_deg: float) -> "Profile":
        """Return a new profile rotated around the origin."""
        from math import radians, cos, sin

        a = radians(angle_deg)
        c, s = cos(a), sin(a)
        return Profile([(x * c - y * s, x * s + y * c) for x, y in self.points])

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


@dataclass
class Revolution:
    """Surface of revolution generated from a 2D profile."""
    profile: Profile
    segments: int = 36

    def to_stl(self) -> str:
        """Return an ASCII STL string of the revolved shape."""
        from math import cos, sin, tau, sqrt

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

        pts = self.profile.points
        lines = ["solid revolution"]
        n = len(pts) - 1
        for s in range(self.segments):
            a1 = tau * s / self.segments
            a2 = tau * (s + 1) / self.segments
            ca1, sa1 = cos(a1), sin(a1)
            ca2, sa2 = cos(a2), sin(a2)
            for i in range(n):
                x1, y1 = pts[i]
                x2, y2 = pts[i + 1]
                p1 = (x1 * ca1, y1, x1 * sa1)
                p2 = (x2 * ca1, y2, x2 * sa1)
                p3 = (x2 * ca2, y2, x2 * sa2)
                p4 = (x1 * ca2, y1, x1 * sa2)
                for tri in ((p1, p2, p3), (p1, p3, p4)):
                    nx, ny, nz = normal(*tri)
                    lines.append(f"facet normal {nx:.6f} {ny:.6f} {nz:.6f}")
                    lines.append("  outer loop")
                    for p in tri:
                        lines.append(f"    vertex {fmt_pt(p)}")
                    lines.append("  endloop")
                    lines.append("endfacet")
        lines.append("endsolid revolution")
        return "\n".join(lines)
