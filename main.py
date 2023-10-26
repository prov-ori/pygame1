import pygame


clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((680, 340)) # , flags=pygame.NOFRAME
pygame.display.set_caption("PYTHON PYGAME GAME1!") # название
#icon = pygame.image.load('images/cannabis.png').convert_alpha() # иконка
#pygame.display.set_icon(icon)

# Player
bg = pygame.image.load('images/background.png').convert_alpha() # задний фон
walk_right = [
    pygame.image.load('images/player_right/player_right1.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right2.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right3.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right4.png').convert_alpha(),
]
walk_left = [
    pygame.image.load('images/player_left/player_left1.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left2.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left3.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left4.png').convert_alpha(),
]

villian = pygame.image.load('images/villian.png').convert_alpha() # злодей
villian_list_in_game = []

player_anim_count = 0
bg_x =0

player_speed = 10
player_x = 150
player_y = 230

is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound('sounds/bgsound.mp3')
bg_sound.play()

villian_timer = pygame.USEREVENT + 1
pygame.time.set_timer(villian_timer, 4000)

label = pygame.font.Font('fonts/BlackOpsOne-Regular.ttf', 40)
lose_label = label.render('You lose!', False, (59, 8, 51))
restart_label = label.render('Restart', False, (33, 24, 32))
restart_label_rect = restart_label.get_rect(topleft=(260, 180))

bullets_left = 10
bullet = pygame.image.load('images/bullet1.png').convert_alpha()
bullets = []

gameplay = True

running = True
while running:

    screen.blit(bg, (bg_x, 0)) # добавляем задний фон
    screen.blit(bg, (bg_x + 680, 0))

    if gameplay:

        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if villian_list_in_game:
            for (i, el) in enumerate(villian_list_in_game):
                screen.blit(villian, el)
                el.x -= 10

                if el.x < -10:
                    villian_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y)) # добавляем  иконку игрока
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 200:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_UP]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count +=1

        bg_x -= 2
        if bg_x == -680:
            bg_x = 0

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 10

                if el.x > 684:
                    bullets.pop(i)

                if villian_list_in_game:
                    for (index, villian_el) in enumerate(villian_list_in_game):
                        if el.colliderect(villian_el):
                            villian_list_in_game.pop(index)
                            bullets.pop(i)
    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (250, 130))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            villian_list_in_game.clear()
            bullets.clear()

    pygame.display.update() # обновляем экран

    for event in pygame.event.get(): # выход из игры
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == villian_timer:
            villian_list_in_game.append(villian.get_rect(topleft=(682, 230)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 70, player_y + 15)))
            bullets_left -= 1

    clock.tick(15)
