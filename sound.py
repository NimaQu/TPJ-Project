import pygame
import threading
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")


def play():
    threading.Thread(target=play_sound, daemon=True).start()


def play_sound():
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue


if __name__ == "__main__":
    while True:
        play_sound()
