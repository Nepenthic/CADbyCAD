# CADbyCAD

A prototype project aiming to combine basic CAD modeling with simple CAM
g-code generation. The goal is to eventually provide the ease of use of
modern CAD packages while also supporting automated toolpath creation.

## Current prototype

The repository contains a small Python module that can load a 2D profile
from a CSV file and either generate g-code or extrude the profile into a
simple 3D model.

### Usage

1. Create a CSV file with one `x,y` pair per line. For example:

   ```
   0,0
   10,0
   10,5
   0,5
   ```

2. Generate g-code:

   ```bash
   python -m cadcam gcode path/to/profile.csv -d 1.0 -f 1000 -p 2 -o output.gcode
   ```

3. Extrude the profile to an STL:

   ```bash
   python -m cadcam stl path/to/profile.csv -H 5 -o part.stl
   ```

The g-code file will contain contouring moves with optional multiple depth
passes. The STL file represents a simple extrusion of the 2D profile.

This code is only a starting point for exploring more advanced features,
including 3D modeling and richer toolpath strategies.
