import argparse
from .model import Profile, Extrusion, Revolution
from .cam import generate_gcode


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple CAD/CAM prototype")
    sub = parser.add_subparsers(dest="command", required=True)

    g = sub.add_parser("gcode", help="Generate G-code from a profile")
    g.add_argument("profile", help="CSV file with x,y coordinates")
    g.add_argument("-d", "--depth", type=float, default=1.0, help="Cut depth")
    g.add_argument("-f", "--feedrate", type=float, default=1000.0, help="Feedrate")
    g.add_argument("-p", "--passes", type=int, default=1, help="Depth passes")
    g.add_argument("-o", "--output", help="Output file (default: stdout)")

    s = sub.add_parser("stl", help="Extrude profile to an STL file")
    s.add_argument("profile", help="CSV file with x,y coordinates")
    s.add_argument("-H", "--height", type=float, required=True, help="Extrusion height")
    s.add_argument("-o", "--output", required=True, help="Output STL file")

    r = sub.add_parser("revolve", help="Revolve profile around the Y axis to STL")
    r.add_argument("profile", help="CSV file with x,y coordinates")
    r.add_argument("-s", "--segments", type=int, default=36, help="Revolution segments")
    r.add_argument("-o", "--output", required=True, help="Output STL file")

    t = sub.add_parser("transform", help="Apply basic transforms to a profile")
    t.add_argument("profile", help="CSV file with x,y coordinates")
    t.add_argument("-T", "--translate", nargs=2, type=float, metavar=("DX","DY"))
    t.add_argument("-S", "--scale", nargs="*", type=float, metavar=("SX","SY"))
    t.add_argument("-R", "--rotate", type=float, help="Rotation angle in degrees")
    t.add_argument("-o", "--output", help="Output CSV file (default: stdout)")

    args = parser.parse_args()

    profile = Profile.from_csv(args.profile)

    if args.command == "gcode":
        gcode = generate_gcode(profile, depth=args.depth, feedrate=args.feedrate, passes=args.passes)
        if args.output:
            with open(args.output, "w") as f:
                f.write(gcode)
        else:
            print(gcode)
    elif args.command == "stl":
        extr = Extrusion(profile, args.height)
        stl = extr.to_stl()
        with open(args.output, "w") as f:
            f.write(stl)
    elif args.command == "revolve":
        rev = Revolution(profile, segments=args.segments)
        stl = rev.to_stl()
        with open(args.output, "w") as f:
            f.write(stl)
    elif args.command == "transform":
        p = profile
        if args.translate:
            p = p.translated(args.translate[0], args.translate[1])
        if args.scale:
            if len(args.scale) == 1:
                p = p.scaled(args.scale[0])
            else:
                p = p.scaled(args.scale[0], args.scale[1])
        if args.rotate is not None:
            p = p.rotated(args.rotate)
        data = "\n".join(f"{x},{y}" for x, y in p.points)
        if args.output:
            with open(args.output, "w") as f:
                f.write(data)
        else:
            print(data)


if __name__ == '__main__':
    main()
