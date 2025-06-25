import argparse
from .model import Profile
from .cam import generate_gcode


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple CAD/CAM prototype")
    parser.add_argument('profile', help='CSV file with x,y coordinates')
    parser.add_argument('-d', '--depth', type=float, default=1.0, help='Cut depth')
    parser.add_argument('-f', '--feedrate', type=float, default=1000.0, help='Feedrate')
    parser.add_argument('-o', '--output', help='Output G-code file (default: stdout)')
    args = parser.parse_args()

    profile = Profile.from_csv(args.profile)
    gcode = generate_gcode(profile, depth=args.depth, feedrate=args.feedrate)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(gcode)
    else:
        print(gcode)


if __name__ == '__main__':
    main()
