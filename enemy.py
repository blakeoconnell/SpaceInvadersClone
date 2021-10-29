from turtle import Turtle
from sounds import SoundEffects
import threading

sounds = SoundEffects()


class EnemyMissile(Turtle):
    def __init__(self, position):
        super().__init__("square")
        self.color("white")
        self.shapesize(stretch_wid=0.1, stretch_len=1)
        self.penup()
        self.moveSpeed = 5
        self.goto(position)
        self.setheading(270)

    def move(self):
        self.forward(self.moveSpeed)

    def made_contact(self):
        self.hideturtle()
        self.goto(4000, 4000)


class Enemy(Turtle):
    def __init__(self, position):
        super().__init__("enemy_ship.gif")
        self.shapesize(stretch_wid=2, stretch_len=2)
        self.penup()
        self.moveSpeed = .44
        self.goto(position)

    def move(self):
        new_x = self.xcor() + self.moveSpeed
        self.goto((new_x, self.ycor()))

    def bounce(self):
        self.moveSpeed *= -1
        new_y = self.ycor() - 20
        self.goto((self.xcor(), new_y))

    def destroy(self):
        x = threading.Thread(target=sounds.enemy_explode, daemon=True)
        x.start()
        self.goto((1000, 1000))

    def fire(self):
        return EnemyMissile((self.xcor(), self.ycor()))
