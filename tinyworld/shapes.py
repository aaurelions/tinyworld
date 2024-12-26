# tinyworld/shapes.py

class Shape:
    def __init__(self, shape_id, x=0, y=0, rotation=0, scale=1.0, opacity=1.0):
        self.shape_id = shape_id
        self.x = x
        self.y = y
        self.rotation = rotation
        self.scale = scale
        self.opacity = opacity

class TextShape(Shape):
    def __init__(self, shape_id, text, x=0, y=0, rotation=0, scale=1.0, opacity=1.0):
        super().__init__(shape_id, x, y, rotation, scale, opacity)
        self.text = text
        self.color = "black"
        self.font = None

class ImageShape(Shape):
    def __init__(self, shape_id, image_path, x=0, y=0, rotation=0, scale=1.0, opacity=1.0):
        super().__init__(shape_id, x, y, rotation, scale, opacity)
        self.image_path = image_path
