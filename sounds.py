from playsound import playsound
import threading

class SoundEffects:
    def __init__(self):
        self.player_explosion = 'sfx_wpn_cannon2.mp3'
        self.player_missile_sound = 'sfx_wpn_laser5.mp3'
        self.enemy_explosion = 'sfx_exp_short_hard14.mp3'
        self.bonus_ship_sound = 'sfx_alarm_loop5.mp3'

    def player_explode(self):
        playsound(self.player_explosion)

    def player_missile(self):
        playsound(self.player_missile_sound)

    def enemy_explode(self):
        playsound(self.enemy_explosion)

    def bonus_ship_active(self):
        playsound(self.bonus_ship_sound)
