import pygame.mixer


class Music:
    current_music = None
    current_volume = 5


pygame.init()


def get_image(file_name):
    file = open(file_name, "r")
    image = file.read()
    file.close()
    return image


def set_volume(volume):
    if volume > 10:
        Music.current_volume = 10
    elif volume < 0:
        Music.current_volume = 0
    else:
        Music.current_volume = volume
    pygame.mixer.music.set_volume(Music.current_volume / 10)


def get_volume():
    return Music.current_volume


def play_music(file_name):
    if current_music() != file_name:
        Music.current_music = file_name
        pygame.mixer.music.load(f'sounds/music/{file_name}')
        pygame.mixer.music.play(-1)


def current_music():
    return Music.current_music


def stop_music():
    pygame.mixer.music.stop()


def play_sound_effect(file_name):
    effect = pygame.mixer.Sound(f'sounds/effects/{file_name}')
    effect.play()
