import pygame
import pygame.surface
import pygame.color
import pygame_gui
import sys


# GUI ELEMENTS
for i in range(9):
    for j in range(9):
        hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((375, 275), (50, 50)),
                                             text='Say Hello',
                                             manager=manager)


# GAME LOOP (UNTIL QUIT EVENT)
running = True
while running:

    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():

        # Quit game
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        # >>>>> KEYSTROKES CONTROL <<<<< #

        # KEY DOWN
        if event.type == pygame.KEYDOWN:
            print('Key pressed down.')

            if event.key == pygame.K_LEFT:
                print('Left key pressed.')
            if event.key == pygame.K_RIGHT:
                print('Right key pressed.')

            if event.type == pygame.K_SPACE:
                print('Space key pressed')

        # KEY UP
        if event.type == pygame.KEYUP:
            print('Key released.')

            if event.key == pygame.K_LEFT or event.key == pygame.K_LEFT:
                print('Key left or right released.')

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == hello_button:
                    print('Hello World!')

        # MANAGER PROCESS
        manager.process_events(event)

    manager.update(time_delta)

    manager.draw_ui(surface)

    pygame.display.update()
