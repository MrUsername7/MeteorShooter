import os

try:
    default_pygame_support_prompt = os.environ['PYGAME_HIDE_SUPPORT_PROMPT']
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
except KeyError:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import random
import pygame

try:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = default_pygame_support_prompt
except NameError:
    os.environ.pop('PYGAME_HIDE_SUPPORT_PROMPT')

SCREEN_WIDTH: int = 512
SCREEN_HEIGHT: int = 512

width_scaling = SCREEN_WIDTH / 128
height_scaling = SCREEN_HEIGHT / 128

pygame.init()
pygame.display.set_caption('Meteor Shooter')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.SysFont('Arial', 36)

ship = {
    'image': pygame.image.load('assets/ship.png'),
    'height': None,
    'width': None,
    'x': None,
    'y': None
}

ship['width'] = ship['image'].get_width() * width_scaling
ship['height'] = ship['image'].get_height() * height_scaling
ship['image'] = pygame.transform.scale(ship['image'], (ship['width'], ship['height']))
ship['x'] = SCREEN_WIDTH // 2 - ship['width'] // 2
ship['y'] = SCREEN_HEIGHT - ship['height']

asteroid = {
    'image': pygame.image.load('assets/asteroid.png'),
    'width': None,
    'height': None,
    'x': None,
    'y': 0
}
asteroid['width'] = asteroid['image'].get_width() * width_scaling
asteroid['height'] = asteroid['image'].get_height() * height_scaling
asteroid['x'] = random.randint(0, int(SCREEN_WIDTH - asteroid['width']))
asteroid['image'] = pygame.transform.scale(asteroid['image'], (asteroid['width'], asteroid['height']))

lasers = {
    'image': pygame.image.load('assets/laser.bmp'),
    'entities': []
}
lasers['image'] = pygame.transform.scale(lasers['image'],
                                         (lasers['image'].get_width() * width_scaling,
                                          lasers['image'].get_height() * height_scaling))
lasers['width'] = lasers['image'].get_width()
lasers['height'] = lasers['image'].get_height()

score = 0

FPS = 60
game_over = False
running = True
while running:
    if not game_over:
        #game over detection
        ship_rect = pygame.Rect(ship['x'], ship['y'], ship['width'], ship['height'])
        asteroid_rect = pygame.Rect(asteroid['x'], asteroid['y'], asteroid['width'], asteroid['height'])
        if pygame.Rect.colliderect(ship_rect, asteroid_rect) or asteroid['y'] > SCREEN_HEIGHT:
            game_over = True

        for i in range(len(lasers['entities'])):
            laser_rect = pygame.Rect(lasers['entities'][i]['x'],
                                     lasers['entities'][i]['y'],
                                     lasers['width'],
                                     lasers['height'])
            if pygame.Rect.colliderect(laser_rect, asteroid_rect):
                score += 1
                lasers['entities'][i]['destroyed'] = True
                asteroid['x'] = random.randint(0, int(SCREEN_WIDTH - asteroid['width']))
                asteroid['y'] = 0

        # move lasers
        for i in range(len(lasers['entities'])):
            lasers['entities'][i]['y'] -= 4
            if lasers['entities'][i]['y'] < -lasers['height']:
                lasers['entities'][i]['destroyed'] = True
        #destroy lasers
        destroyed_lasers_exist = True
        while destroyed_lasers_exist and len(lasers['entities']) > 0:
            for i in range(len(lasers['entities'])):
                if lasers['entities'][i]['destroyed']:
                    lasers['entities'].pop(i)
                    break
                elif i == len(lasers['entities']) - 1:
                    destroyed_lasers_exist = False

    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                lasers['entities'].append({
                    'x': ship['x'] + (ship['width'] // 2) - (lasers['width'] // 2),
                    'y': SCREEN_HEIGHT - ship['height'] - lasers['height'],
                    'destroyed': False
                })
    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if ship['x'] > 4:
                ship['x'] -= 4
            else:
                ship['x'] = 0
        if keys[pygame.K_RIGHT]:
            if ship['x'] < SCREEN_WIDTH - ship['width'] - 4:
                ship['x'] += 4
            else:
                ship['x'] = SCREEN_WIDTH - ship['width']

        #move asteroid
        asteroid['y'] += 0.5

        # render the scene
        screen.fill((0, 0, 0))
        screen.blit(asteroid['image'], (asteroid['x'], asteroid['y']))
        for i in lasers['entities']:
            screen.blit(lasers['image'], (i['x'], i['y']))
        screen.blit(ship['image'], (ship['x'], ship['y']))
        score_text = font.render('Score: ' + str(score), True, (255, 255, 255))
        screen.blit(score_text, (0, 0))
    else:
        game_over_text = font.render('Game Over!', True, (255, 255, 255))
        screen.blit(game_over_text,
                    (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                          SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

pygame.quit()
