import enemy
import util


class EnemyFactory:
    WEAK_ENEMY_TYPES = ('R', 'S', 's')
    STRONG_ENEMY_TYPES = ('G', 'K', 'M', 'n')
    MINIBOSS_TYPES = ()
    BOSS_TYPES = ('D',)
    ALL_ENEMY_TYPES = WEAK_ENEMY_TYPES + STRONG_ENEMY_TYPES + MINIBOSS_TYPES + BOSS_TYPES

    def get(self, enemy_type, level):
        if enemy_type == 'D':
            new_enemy = enemy.Dragon(level)
            new_enemy.battle_music = 'boss_song.wav'
        elif enemy_type == 'n':
            new_enemy = enemy.Demon(level)
            new_enemy.battle_music = 'miniboss_song.wav'
        elif enemy_type == 'G':
            new_enemy = enemy.Gargoyle(level)
        elif enemy_type == 'K':
            new_enemy = enemy.Knight(level)
        elif enemy_type == 'M':
            new_enemy = enemy.Minotaur(level)
        elif enemy_type == 'R':
            new_enemy = enemy.Rat(level)
        elif enemy_type == 'S':
            new_enemy = enemy.Skeleton(level)
        elif enemy_type == 's':
            new_enemy = enemy.Spider(level)
        else:
            new_enemy = None

        if new_enemy.battle_music is None:
            new_enemy.battle_music = 'battle_song.wav'

        if new_enemy is not None:
            img = f'images/enemy/{new_enemy.__class__.__name__.lower()}.txt'
            new_enemy.image = util.get_image(img)
        new_enemy.scale_stats()
        return new_enemy
