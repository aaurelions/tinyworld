# tinyworld/transitions.py

class Transition:
    def __init__(self, shape_id, start_time, end_time):
        self.shape_id = shape_id
        self.start_time = start_time
        self.end_time = end_time

class FadeIn(Transition):
    def __init__(self, shape_id, start_time, end_time):
        super().__init__(shape_id, start_time, end_time)

class FadeOut(Transition):
    def __init__(self, shape_id, start_time, end_time):
        super().__init__(shape_id, start_time, end_time)

class Move(Transition):
    def __init__(self, shape_id, start_time, end_time, start_pos, end_pos):
        super().__init__(shape_id, start_time, end_time)
        self.start_pos = start_pos
        self.end_pos = end_pos

class Rotate(Transition):
    def __init__(self, shape_id, start_time, end_time, start_angle, end_angle):
        super().__init__(shape_id, start_time, end_time)
        self.start_angle = start_angle
        self.end_angle = end_angle

class Scale(Transition):
    def __init__(self, shape_id, start_time, end_time, start_scale, end_scale):
        super().__init__(shape_id, start_time, end_time)
        self.start_scale = start_scale
        self.end_scale = end_scale
