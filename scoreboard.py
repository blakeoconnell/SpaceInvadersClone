from turtle import Turtle


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color('white')
        self.penup()
        self.hideturtle()
        self.score = 0
        self.high_score = 624
        self.lives = 3
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(-200, 350)
        self.write(f'Score: {self.score}', align='center', font=('Atari Classic', 18, 'normal'))
        self.goto(135, 350)
        self.write(f'High Score: {self.high_score}', align='center', font=('Atari Classic', 18, 'normal'))
        self.goto(-220, -360)
        self.write(f'Lives: {self.lives}', align='center', font=('Atari Classic', 18, "normal"))

    def lose_life(self):
        self.lives -= 1
        self.update_scoreboard()

    def score_points(self, points):
        self.score += points
        self.update_scoreboard()

    def set_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

    def win(self):
        self.home()
        self.write("You win!", align='center', font=('Courier', 60, 'normal'))

    def lose(self):
        self.home()
        self.write("You lose.", align='center', font=('Courier', 60, 'normal'))