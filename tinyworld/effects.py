# tinyworld/effects.py

class FX:
    """Base class for advanced cross-scene effects (like transitions between entire scenes)."""
    pass

class CrossFade(FX):
    """
    Crossfades from scene A to scene B (not yet integrated in the pipeline).
    You could implement by stacking frames from both scenes in a transitional region
    or using MoviePy composition.
    """
    pass

class Slide(FX):
    """
    Slide from one scene to the next horizontally/vertically.
    """
    pass

class Wipe(FX):
    """
    Wipe from one scene to another.
    """
    pass
