import sys
import random

import pygame
import pygame.mixer

from classes.constants import WIDTH, HEIGHT, BLACK, WHITE, RED


# Global setting for background mode
background_mode = "classic"  # "classic" or "dynamic"


def get_background_mode():
    return background_mode


def animate_screen():
    for i in range(0, 20):
        screen.blit(mainmenu_img, (0, 0))
        pygame.display.flip()
        pygame.time.wait(10)
        screen.blit(mainmenu_img, (random.randint(-5, 5), random.randint(-5, 5)))
        pygame.display.flip()
        pygame.time.wait(10)


pygame.mixer.init()
pygame.init()
pygame.mixer.music.load('game_sounds/menu.mp3')
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)
pygame.mixer.set_num_channels(20)
for i in range(20):
    channel = pygame.mixer.Channel(i)
    channel.set_volume(0.25)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()

mainmenu_img = pygame.image.load('images/mainmenu.jpg').convert()
mainmenu_img = pygame.transform.scale(mainmenu_img, (WIDTH, HEIGHT))

logo_img = pygame.image.load('images/ch.png').convert_alpha()
logo_x = (WIDTH - logo_img.get_width()) // 2
logo_y = 50

# Button positions
play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 205, 50)
bg_mode_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 205, 50)
quit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 125, 205, 50)

pygame.mixer.music.load('game_sounds/menu.mp3')
pygame.mixer.music.play(-1)
explosion_sound = pygame.mixer.Sound('game_sounds/explosions/explosion1.wav')
explosion_sound.set_volume(0.25)
selected_button = 0
show_menu = True

joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()


def toggle_background_mode():
    global background_mode
    if background_mode == "classic":
        background_mode = "dynamic"
    else:
        background_mode = "classic"


def get_bg_mode_text():
    return f"BG: {background_mode.capitalize()}"


while show_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if play_button_rect.collidepoint(x, y):
                explosion_sound.play()
                animate_screen()
                show_menu = False
                break
            elif bg_mode_button_rect.collidepoint(x, y):
                toggle_background_mode()
            elif quit_button_rect.collidepoint(x, y):
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_button = (selected_button - 1) % 3
            elif event.key == pygame.K_DOWN:
                selected_button = (selected_button + 1) % 3
            elif event.key == pygame.K_RETURN:
                if selected_button == 0:
                    explosion_sound.play()
                    animate_screen()
                    show_menu = False
                    screen.fill(BLACK)
                    break
                elif selected_button == 1:
                    toggle_background_mode()
                elif selected_button == 2:
                    pygame.quit()
                    sys.exit()
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                if selected_button == 1:
                    toggle_background_mode()

        if joystick:
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    if selected_button == 0:
                        explosion_sound.play()
                        animate_screen()
                        show_menu = False
                        screen.fill(BLACK)
                        break
                    elif selected_button == 1:
                        toggle_background_mode()
                    elif selected_button == 2:
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.JOYHATMOTION:
                if event.value[1] == 1:
                    selected_button = (selected_button - 1) % 3
                elif event.value[1] == -1:
                    selected_button = (selected_button + 1) % 3
                elif event.value[0] != 0 and selected_button == 1:
                    toggle_background_mode()

    screen.blit(mainmenu_img, (0, 0))
    screen.blit(logo_img, (logo_x, logo_y))

    font = pygame.font.SysFont('Comic Sans MS', 40)
    font_small = pygame.font.SysFont('Comic Sans MS', 28)

    # Play button
    text = font.render("Play", True, WHITE)
    pygame.draw.rect(screen, BLACK, play_button_rect, border_radius=10)
    if selected_button == 0:
        pygame.draw.rect(screen, RED, play_button_rect, border_radius=10, width=4)
    text_rect = text.get_rect()
    text_rect.center = play_button_rect.center
    screen.blit(text, text_rect)

    # Background mode button
    bg_text = font_small.render(get_bg_mode_text(), True, WHITE)
    pygame.draw.rect(screen, BLACK, bg_mode_button_rect, border_radius=10)
    if selected_button == 1:
        pygame.draw.rect(screen, RED, bg_mode_button_rect, border_radius=10, width=4)
    # Add left/right arrows to indicate it's toggleable
    arrow_font = pygame.font.SysFont('Comic Sans MS', 28)
    left_arrow = arrow_font.render("<", True, WHITE)
    right_arrow = arrow_font.render(">", True, WHITE)
    screen.blit(left_arrow, (bg_mode_button_rect.left + 10, bg_mode_button_rect.centery - 12))
    screen.blit(right_arrow, (bg_mode_button_rect.right - 25, bg_mode_button_rect.centery - 12))
    bg_text_rect = bg_text.get_rect()
    bg_text_rect.center = bg_mode_button_rect.center
    screen.blit(bg_text, bg_text_rect)

    # Exit button
    text = font.render("Exit", True, WHITE)
    pygame.draw.rect(screen, BLACK, quit_button_rect, border_radius=10)
    if selected_button == 2:
        pygame.draw.rect(screen, RED, quit_button_rect, border_radius=10, width=4)
    text_rect = text.get_rect()
    text_rect.center = quit_button_rect.center
    screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
