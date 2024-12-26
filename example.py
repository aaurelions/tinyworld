# example.py
# Minimal demonstration: Programmatically calls the CLI logic
# Or you can just do: tinyworld example.json

from tinyworld.cli import main

if __name__ == "__main__":
    import sys
    sys.argv = ["tinyworld", "example.json"]
    main()
