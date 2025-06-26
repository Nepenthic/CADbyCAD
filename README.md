# CADbyCAD

A prototype project aiming to combine basic CAD modeling with simple CAM
g-code generation. The goal is to eventually provide the ease of use of
modern CAD packages while also supporting automated toolpath creation.

## Current prototype

The repository contains a small Python module that can load a 2D profile
from a CSV file and either generate g-code or create basic 3D models. The
current tooling is intentionally tiny but aims to gradually grow into a
more capable CAD/CAM environment.

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

4. Revolve the profile around the Y axis:

   ```bash
   python -m cadcam revolve path/to/profile.csv -s 36 -o part.stl
   ```

5. Apply simple transformations (translate, scale or rotate) and output a new
   profile:

   ```bash
   python -m cadcam transform path/to/profile.csv -T 5 2 -S 2 -R 45 -o new.csv
   ```

6. Launch the graphical interface:

   ```bash
   python -m cadcam gui
   ```
   (Requires Tkinter and a desktop environment.)

The g-code file will contain contouring moves with optional multiple depth
passes. The STL file represents a simple extrusion of the 2D profile.

This code is only a starting point for exploring more advanced features,
including 3D modeling and richer toolpath strategies.
