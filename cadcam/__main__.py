import argparse
from .model import Profile, Extrusion
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


if __name__ == '__main__':
    main()
