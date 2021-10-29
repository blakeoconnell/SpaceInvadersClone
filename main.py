import turtle
from turtle import Screen
from player import Player
from enemy import Enemy
from bonus import BonusShip
from defense import Defense
from scoreboard import Scoreboard
from sounds import SoundEffects
import threading
import random
import time


screen = Screen()

screen.bgcolor("black")
screen.setup(672, 768)
screen.title("Space Invaders")
screen.tracer(0)

turtle.register_shape("enemy_ship.gif")
turtle.register_shape("bonus_ship.gif")
turtle.register_shape("player_ship.gif")


# set enemies
def set_enemies():
    new_enemies = []
    x = -260
    y = 250
    for j in range(4):
        for i in range(11):
            new_enemy = Enemy((x, y))
            new_enemies.append(new_enemy)
            x += 50
        x = -260
        y -= 50
    return new_enemies


# set defense
def set_defense():
    new_defense = []
    base_x = -210
    x = -210
    y = -200
    row_length = 8
    for j in range(2):
        for i in range(row_length):
            new_block = Defense((x, y))
            new_defense.append(new_block)
            x += 6
        base_x -= 3
        x = base_x
        y -= 6
        row_length += 1
    for j in range(5):
        for i in range(row_length):
            new_block = Defense((x, y))
            new_defense.append(new_block)
            x += 6
        x = base_x
        y -= 6
    for j in range(3):
        for i in range(row_length):
            if -200 > x or x > -180:
                new_block = Defense((x, y))
                new_defense.append(new_block)
            x += 6
        x = base_x
        y -= 6
    base_x = -80
    x = -80
    y = -200
    row_length = 8
    for j in range(2):
        for i in range(row_length):
            new_block = Defense((x, y))
            new_defense.append(new_block)
            x += 6
        base_x -= 3
        x = base_x
        y -= 6
        row_length += 1
    for j in range(5):
        for i in range(row_length):
            new_block = Defense((x, y))
            new_defense.append(new_block)
            x += 6
        x = base_x
        y -= 6
    for j in range(3):
        for i in range(row_length):
            if -70 > x or x > -50:
                new_block = Defense((x, y))
                new_defense.append(new_block)
            x += 6
        x = base_x
        y -= 6
    base_x = 50
    x = 50
    y = -200
    row_length = 8
    for j in range(2):
        for i in range(row_length):
            new_block = Defense((x, y))
            new_defense.append(new_block)
            x += 6
        base_x -= 3
        x = base_x
        y -= 6
        row_length += 1
    for j in range(5):
        for i in range(row_length):
            new_block = Defense((x, y))
            new_defense.append(new_block)
            x += 6
        x = base_x
        y -= 6
    for j in range(3):
        for i in range(row_length):
            if 60 > x or x > 80:
                new_block = Defense((x, y))
                new_defense.append(new_block)
            x += 6
        x = base_x
        y -= 6
    base_x = 180
    x = 180
    y = -200
    row_length = 8
    for j in range(2):
        for i in range(row_length):
            new_block = Defense((x, y))
            new_defense.append(new_block)
            x += 6
        base_x -= 3
        x = base_x
        y -= 6
        row_length += 1
    for j in range(5):
        for i in range(row_length):
            new_block = Defense((x, y))
            new_defense.append(new_block)
            x += 6
        x = base_x
        y -= 6
    for j in range(3):
        for i in range(row_length):
            if 190 > x or x > 210:
                new_block = Defense((x, y))
                new_defense.append(new_block)
            x += 6
        x = base_x
        y -= 6
    return new_defense


player = Player((0, -300))
enemies = set_enemies()
defenses = set_defense()
scoreboard = Scoreboard()
sounds = SoundEffects()

# keybindings
screen.listen()
screen.getcanvas().bind('<Left>', player.move_left)
screen.getcanvas().bind('<Right>', player.move_right)
screen.getcanvas().bind('<space>', player.fire)
screen.getcanvas().winfo_pointerx()

game_is_on = True
sleep_amount = 0.00001
passes = 0
enemies_destroyed = 0
enemy_missiles = []
wall_contact = False
wall_contact_right = True
bonus_ship_active = False
level = 1

while game_is_on:

    enemy_move_speed = .22 * (1 + ((level * .1) * enemies_destroyed))

    passes += 1
    time.sleep(sleep_amount)
    screen.update()

    if not bonus_ship_active and enemies_destroyed % 11 == 0 and enemies_destroyed != 0:
        bonus_ship_active = True
        # left or right choice
        randShip = random.randint(1, 2)
        if randShip == 1:
            bonus_ship = BonusShip((-380, 300), 0)
        else:
            bonus_ship = BonusShip((380, 300), 180)

    if bonus_ship_active:
        bonus_ship.move()

        # out of bounds
        if bonus_ship.xcor() > 390 or bonus_ship.xcor() < -390:
            bonus_ship.reset_ship()
            bonus_ship_active = False

    for missile in player.missiles:
        missile.move()

        # missile contact north wall
        if missile.ycor() > 380:
            player.missile_destroyed(missile)

        # missile contact bonus ship
        if bonus_ship_active and missile.distance(bonus_ship) < 40:
            player.missile_destroyed(missile)
            bonus_ship.destroy()
            del bonus_ship
            bonus_ship_active = False
            scoreboard.score_points(100)

    for missile in enemy_missiles:
        missile.move()

        # missile contact south wall
        if missile.ycor() < -380:
            missile.made_contact()
            enemy_missiles.remove(missile)

        # missile contact player missile
        if len(player.missiles) > 0 and missile.distance(player.missiles[0]) < 10:
            player.missile_destroyed(player.missiles[0])
            missile.made_contact()
            enemy_missiles.remove(missile)

        # missile contact with player
        if missile.distance(player) < 15:
            x = threading.Thread(target=sounds.player_explode, daemon=True)
            x.start()
            time.sleep(2)
            missile.made_contact()
            enemy_missiles.remove(missile)
            scoreboard.lose_life()
            player.set_position((0, -300))

    for defense in defenses:
        if len(player.missiles) > 0 and defense.distance(player.missiles[0]) < 10:
            defense.destroy()
            player.missile_destroyed(player.missiles[0])

        for missile in enemy_missiles:
            if defense.distance(missile) < 15:
                defense.destroy()
                missile.made_contact()
                enemy_missiles.remove(missile)

    for enemy in enemies:
        if enemy.moveSpeed < 0:
            enemy.moveSpeed = enemy_move_speed * -1
        else:
            enemy.moveSpeed = enemy_move_speed
        enemy.move()

        # Check wall contact right
        if enemy.xcor() > 310 and wall_contact_right:
            wall_contact = True
            wall_contact_right = False

        # Check wall contact left
        if enemy.xcor() < -310 and not wall_contact_right:
            wall_contact = True
            wall_contact_right = True

        # PLAYER MISSILE CONTACT
        if len(player.missiles) > 0 and enemy.distance(player.missiles[0]) < 25:
            scoreboard.score_points(23)
            enemy.destroy()
            enemies_destroyed += 1
            enemy.moveSpeed = enemy.moveSpeed + (.01 * enemies_destroyed)
            enemies.remove(enemy)
            player.missile_destroyed(player.missiles[0])

        # Bottom wall contact (game over, player loses)
        if enemy.ycor() < -360 or scoreboard.lives == 0:
            scoreboard.lose()
            for enemy_ in enemies:
                enemy.destroy()
            for defense_ in defenses:
                defense_.destroy()
            player.hideturtle()
            if bonus_ship_active:
                bonus_ship.hideturtle()
            game_is_on = False

    if wall_contact:
        for enemy in enemies:
            enemy.bounce()
    wall_contact = False

    if passes % 50 == 0:
        firing_enemy = random.choice(enemies)
        enemy_missiles.append(firing_enemy.fire())

    if not enemies:
        scoreboard.win()
        scoreboard.set_high_score()
        game_is_on = False


screen.exitonclick()
