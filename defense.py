from turtle import Turtle


class Defense(Turtle):
    def __init__(self, position):
        super().__init__("square")
        self.position = position
        self.color("green")
        self.penup()
        self.shapesize(stretch_wid=0.25, stretch_len=0.25)
        self.goto(position)

    def destroy(self):
        self.goto(8000, 8000)
