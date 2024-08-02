# run.py
import argparse
from SelectMode import ModeSelector

def main():
    parser = argparse.ArgumentParser(description="Select the mode to run the application.")
    parser.add_argument("mode", choices=["gui", "web"], help="Mode to run the application in.")
    args = parser.parse_args()

    mode_function = ModeSelector(args.mode)
    mode_function()

if __name__ == "__main__":
    main()
