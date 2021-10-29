from turtle import Turtle
from sounds import SoundEffects
import threading

sounds = SoundEffects()


class BonusShip(Turtle):
    def __init__(self, position, heading):
        super().__init__("bonus_ship.gif")
        self.color("red")
        self.shapesize(stretch_wid=1, stretch_len=3)
        self.penup()
        self.moveSpeed = 2
        self.goto(position)
        self.setheading(heading)

    def move(self):
        self.forward(self.moveSpeed)

    def destroy(self):
        x = threading.Thread(target=sounds.enemy_explode, daemon=True)
        x.start()
        self.goto(6000, 6000)

    def reset_ship(self):
        self.goto(6000, 6000)
