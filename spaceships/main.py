import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Starships")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
pygame.mixer.Sound.set_volume(BULLET_HIT_SOUND, 0.2)
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
pygame.mixer.Sound.set_volume(BULLET_FIRE_SOUND, 0.2)

HEALTH_FONT = pygame.font.SysFont('bankgothic', 40)
WINNER_FONT = pygame.font.SysFont('yugothicregular', 100)

SPACESHIP_HEIGHT = 66
SPACESHIP_WIDTH = 53
FPS = 60
VEL = 6
BULLET_VEL = 7
MAX_BULLETS = 8

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)), 270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
        
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    
    pygame.display.update()
    
def yellow_handle_movement(keys_pressed, yellow):
        if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # left, closer to 0,0
            yellow.x -= VEL
        if keys_pressed[pygame.K_d] and yellow.x + VEL < (BORDER.x - SPACESHIP_WIDTH): # right
            yellow.x += VEL
        if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # up
            yellow.y -= VEL
        if keys_pressed[pygame.K_s] and yellow.y + VEL < (HEIGHT - SPACESHIP_HEIGHT): # down
            yellow.y += VEL
            
def red_handle_movement(keys_pressed, red):
        if keys_pressed[pygame.K_l] and red.x - VEL > (BORDER.x + BORDER.width): # left, closer to 0,0
            red.x -= VEL
        if keys_pressed[pygame.K_QUOTE] and red.x + VEL < (WIDTH - SPACESHIP_WIDTH): # right
            red.x += VEL
        if keys_pressed[pygame.K_p] and red.y - VEL > 0: # up
            red.y -= VEL
        if keys_pressed[pygame.K_SEMICOLON] and red.y + VEL < (HEIGHT - SPACESHIP_HEIGHT): # down
            red.y += VEL
            
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL #move
        if red.colliderect(bullet): #check collision
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
            
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL #move
        if yellow.colliderect(bullet): #check collision
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(750, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(250, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []
    
    red_health = 6
    yellow_health = 6
    
    clock = pygame.time.Clock()
    # game loop
    run = True
    while run:
        # caps fps at 60
        clock.tick(FPS)
        # check if close window with red(X)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + SPACESHIP_WIDTH, yellow.y + SPACESHIP_HEIGHT // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + SPACESHIP_HEIGHT // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
                
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
                
        winner_text = ""
        if red_health <= 0:
            winner_text = "YELLOW WINS!"
            
        if yellow_health <= 0:
            winner_text = "RED WINS!"
            
        if winner_text != "":
            draw_winner(winner_text)
            break
        
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        
    main()

    
if __name__ == "__main__":
    main()