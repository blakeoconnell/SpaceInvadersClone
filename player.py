from turtle import Turtle
from sounds import SoundEffects
import threading

sounds = SoundEffects()


class PlayerMissile(Turtle):
    def __init__(self, position):
        super().__init__("square")
        self.color("white")
        self.shapesize(stretch_wid=0.1, stretch_len=1)
        self.penup()
        self.moveSpeed = 15
        self.goto(position)
        self.setheading(90)

    def move(self):
        self.forward(self.moveSpeed)

    def made_contact(self):
        self.hideturtle()
        self.goto(2000, 2000)


class Player(Turtle):
    def __init__(self, position):
        self.missiles = []
        super().__init__("player_ship.gif")
        self.penup()
        self.moveSpeed = 10
        self.set_position(position)

    def move_left(self, event):
        new_x = self.xcor() - self.moveSpeed
        self.goto((new_x, self.ycor()))

    def move_right(self, event):
        new_x = self.xcor() + self.moveSpeed
        self.goto((new_x, self.ycor()))

    def set_position(self, position):
        self.goto(position)

    def fire(self, event):
        if len(self.missiles) == 0:
            new_missile = PlayerMissile((self.xcor(), self.ycor()))
            # thread missile so it does not halt the game
            x = threading.Thread(target=sounds.player_missile, daemon=True)
            x.start()
            self.missiles.append(new_missile)

    def missile_destroyed(self, missile):
        # thread missile so it does not halt the game
        x = threading.Thread(target=sounds.enemy_explode, daemon=True)
        x.start()
        missile.made_contact()
        self.missiles.remove(missile)
