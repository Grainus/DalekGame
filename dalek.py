

class Dalek:
    def __init__(self):
        self.is_alive = True
        self.move_count=0

    def explode(self):
        self.is_alive = False