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
