import sys
import pygame
from random import choice
from content.Player import Player
from content.Obstacle import Obstacle


def display_score():
    time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = font.render(f"Score: {time}", False, (64, 64, 64)).convert()
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return time


def collision():
    if pygame.sprite.spritecollide(player.sprite, obstacle, False):
        obstacle.empty()
        return False
    else:
        return True


pygame.init()
pygame.display.set_caption("Jumping Runner")

screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
font = pygame.font.Font("./Jumping_Game/font/Pixeltype.ttf", 50)
bg_music = pygame.mixer.Sound("./Jumping_Game/audio/music.wav")
bg_music.set_volume(0.1)
bg_music.play(loops=-1)

# Load all our graphics
# The convert() method converts the image to a format that is easier for the computer to understand

sky_surface = pygame.image.load("./Jumping_Game/graphics/Sky.png").convert()
ground_surface = pygame.image.load("./Jumping_Game/graphics/ground.png").convert()

# The rectangle is the area that the image takes up
# This can use arguments like width, height, top, bottom, left, right, center, midbottom, midtop, midleft, midright to position the character easily
# The rectangle is used to position the image on the screen and to detect collisions

player = pygame.sprite.GroupSingle()
player.add(Player())

# Obstacles
obstacle = pygame.sprite.Group()

# Intro screen
player_stand = pygame.image.load("./Jumping_Game/graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

title_surface = font.render("Pixel Runner", False, (111, 196, 169)).convert()
title_rect = title_surface.get_rect(center=(400, 80))

start_surface = font.render("Press space to start", False, (111, 196, 169)).convert()
start_rect = start_surface.get_rect(center=(400, 330))

# Game variables
game_active = False
start_time = 0
score = 0

# Timer for obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if game_active:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == obstacle_timer:
                obstacle.add(Obstacle(choice(["snail", "snail", "snail", "fly"])))

        else:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_time = int(pygame.time.get_ticks() / 1000)
                game_active = True

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle.draw(screen)
        obstacle.update()

        game_active = collision()

    else:
        screen.fill((94, 129, 162))
        score_surface = font.render(
            f"Your score: {score}", False, (111, 196, 169)
        ).convert()
        score_rect = score_surface.get_rect(center=(400, 330))

        screen.blit(title_surface, title_rect)
        screen.blit(player_stand, player_stand_rect)

        if score == 0:
            screen.blit(start_surface, start_rect)
        else:
            screen.blit(score_surface, score_rect)

    # Draw all Our elements
    # Update the screen
    pygame.display.update()

    # The clock is telling the while this should run 60 times a second
    # In other words, it will run 60 frames per second
    clock.tick(60)
