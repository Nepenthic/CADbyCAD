# CADbyCAD

A prototype project aiming to combine basic CAD modeling with simple CAM
g-code generation. The goal is to eventually provide the ease of use of
modern CAD packages while also supporting automated toolpath creation.

## Current prototype

The repository contains a minimal Python module that can load a 2D profile
from a CSV file and generate basic g-code for tracing the shape.

### Usage

1. Create a CSV file with one `x,y` pair per line. For example:

   ```
   0,0
   10,0
   10,5
   0,5
   ```

2. Run the prototype:

   ```bash
   python -m cadcam path/to/profile.csv -d 1.0 -f 1000 -o output.gcode
   ```

This will create a `output.gcode` file with simple commands for cutting
the supplied profile at the given depth and feedrate.

This code is only a starting point for exploring more advanced features,
including 3D modeling and richer toolpath strategies.
