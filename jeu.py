#!/bin/python3

"inspiré de : https://pygame.readthedocs.io/en/latest/rect/rect.html#virtual-attributes"

import pygame

width = height= 1000
RED = (255, 0, 0)
#GREEN = (0, 255, 0)
#BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
#MAGENTA = (255, 0, 255)
#CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
#GRAY = (150, 150, 150)
#WHITE = (255, 255, 255)

delay = 50
speed_cat = (width + height)//200
speed_mouse = speed_cat*2
taille_cat = (width + height)//14
taille_mouse = (width + height)//28
start_mouse = [0, 0]
start_cat = [width//2 - taille_cat//2, height//2 - taille_cat//2]
directions_mouse = start_mouse
directions_cat = start_cat
score = 0
pause = True
game_over = False

pygame.init()
screen = pygame.display.set_mode((width, height))
myfont = pygame.font.SysFont('monospace', width//20)
mysubfont = pygame.font.SysFont('monospace', width//40)
running = True

screen = pygame.display.set_mode((width, height)) 

wallpap = pygame.image.load('wallpap.jpg')
wallpap = pygame.transform.scale(wallpap,(width,height))
rect_wallpap = wallpap.get_rect()

img_cat = pygame.image.load('cat.png')
img_cat = pygame.transform.scale(img_cat,(taille_cat,taille_cat))
rect_cat = img_cat.get_rect()
(w, h) = screen.get_size()
flipped = True

img_mouse = pygame.image.load('mouse.png')
img_mouse = pygame.transform.scale(img_mouse,
                                    (taille_mouse + taille_mouse//3,
                                    taille_mouse)
                                    )
rect_mouse = img_mouse.get_rect()

bord_haut = pygame.Rect(0, -1, width, 1)
bord_bas = pygame.Rect(0, height, width, 1)
bord_gauche = pygame.Rect(0, 0, -1, height)
bord_droit = pygame.Rect(width, 0, 1, height)
bords = [bord_haut, bord_bas, bord_gauche, bord_droit]


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    key = pygame.key.get_pressed()
    
    
    
    if not pause and not game_over:
        screen.blit(wallpap,rect_wallpap)

        if key[pygame.K_UP] and key[pygame.K_LEFT]:
            directions_cat = [-speed_cat, -speed_cat]
        elif key[pygame.K_UP] and key[pygame.K_RIGHT]:
            directions_cat = [speed_cat, -speed_cat]
        elif key[pygame.K_DOWN] and key[pygame.K_LEFT]:
            directions_cat = [-speed_cat, speed_cat]
        elif key[pygame.K_DOWN] and key[pygame.K_RIGHT]:
            directions_cat = [speed_cat, speed_cat]
        else:
            if key[pygame.K_UP]:
                directions_cat = [0, -speed_cat]
            if key[pygame.K_DOWN]:
                directions_cat = [0, speed_cat]
            if key[pygame.K_LEFT]:
                directions_cat = [-speed_cat, 0]
            if key[pygame.K_RIGHT]:
                directions_cat = [speed_cat, 0]

        if key[pygame.K_z]:
            directions_mouse = [0, -speed_mouse]
        if key[pygame.K_s]:
            directions_mouse = [0, speed_mouse]
        if key[pygame.K_q]:
            directions_mouse = [-speed_mouse, 0]
        if key[pygame.K_d]:
            directions_mouse = [speed_mouse, 0]

        if score == 0 or not score % 25:
            score_txt = myfont.render("Score : "+str(score), False, YELLOW)
        screen.blit(score_txt,
                    (width//2 - score_txt.get_width()//2,
                    height - score_txt.get_height())
                    )
        score += 1

        mem_cat = (rect_cat.x, rect_cat.y)
        rect_cat = rect_cat.move(directions_cat)
        if rect_cat.collidelist(bords) != -1 :
            (rect_cat.x, rect_cat.y) = mem_cat
        directions_cat = [0, 0]
        
        mem_mouse = (rect_mouse.x, rect_mouse.y)
        rect_mouse = rect_mouse.move(directions_mouse)
        if rect_mouse.collidelist(bords) != -1 :
            (rect_mouse.x, rect_mouse.y) = mem_mouse
        directions_mouse = [0, 0]
        
        screen.blit(img_mouse, rect_mouse)
        screen.blit(img_cat, rect_cat)

        if rect_cat < rect_mouse and not flipped:
            img_cat = pygame.transform.flip(img_cat, True, False)
            img_mouse = pygame.transform.flip(img_mouse, True, False)
            flipped = True
        elif rect_cat > rect_mouse and flipped:
            img_cat = pygame.transform.flip(img_cat, True, False)
            img_mouse = pygame.transform.flip(img_mouse, True, False)
            flipped = False

        if key[pygame.K_SPACE]:
            pause = True


        if rect_cat.colliderect(rect_mouse) :
            game_over = True
#            pygame.draw.rect(screen, GREEN, rect_mouse)
#            pygame.draw.rect(screen, BLUE, rect_cat))
            screen.blit(img_mouse, rect_mouse)
            screen.blit(img_cat, rect_cat)
            rect_clip = rect_cat.clip(rect_mouse)
            pygame.draw.rect(screen, RED, rect_clip)
            game_over_txt = myfont.render("The Cat Won", False, YELLOW)
            replay_txt = myfont.render("Press 'R' to Retry", False, YELLOW)
            quit_txt = myfont.render("Press 'esc' to Quit", False, YELLOW)
            score_txt = myfont.render("Score : "+str(score), False, YELLOW)
            screen.blit(game_over_txt,
                        (width//2-game_over_txt.get_width()//2,
                         0)
                        )
            screen.blit(replay_txt,
                        (width//2-replay_txt.get_width()//2,
                         height - 300)
                        )
            screen.blit(quit_txt,
                        (width//2-quit_txt.get_width()//2,
                         height - 200)
                        )
            screen.fill(BLACK,
                        (0,
                        height - score_txt.get_height(),
                        width,
                        250)
                        )
            screen.blit(score_txt,
                        (width//2 - score_txt.get_width()//2 ,
                        height - score_txt.get_height())
                        )

    if pause:
        screen.fill(BLACK)
        pause_txt = myfont.render("Paused", False, YELLOW)
        mouse_tip_txt = myfont.render("For the mouse: ", False, YELLOW)
        mouse_tip2_txt = mysubfont.render("Move with ZQSD", False, YELLOW)
        mouse_tip3_txt = mysubfont.render("Don't get caught by the cat", False, YELLOW)
        mouse_tip4_txt = mysubfont.render("Try to get the highest score possible", False, YELLOW)
        cat_tip_txt = myfont.render("For the cat: ", False, YELLOW)
        cat_tip2_txt = mysubfont.render("Move with the arrows", False, YELLOW)
        cat_tip3_txt = mysubfont.render("Catch the mouse", False, YELLOW)
        cat_tip4_txt = mysubfont.render("Try to get the lowest score possible", False, YELLOW)
        pause_txt = myfont.render("Paused", False, YELLOW)
        return_txt = myfont.render("Press 'return' to Play", False, YELLOW)
        screen.blit(pause_txt,
                    (width//2-pause_txt.get_width()//2,0)
                    )
        screen.blit(return_txt,
                    (width//2-return_txt.get_width()//2,
                    height - return_txt.get_height())
                    )
        screen.blit(mouse_tip_txt,
            (width//50, 100))
        screen.blit(mouse_tip2_txt,
            (width//25, 150))
        screen.blit(mouse_tip3_txt,
            (width//25, 200))
        screen.blit(mouse_tip4_txt,
            (width//25, 250))
        screen.blit(cat_tip_txt,
            (width//50, 350))
        screen.blit(cat_tip2_txt,
            (width//25, 400))
        screen.blit(cat_tip3_txt,
            (width//25, 450))
        screen.blit(cat_tip4_txt,
            (width//25, 500))


    if key[pygame.K_RETURN] and not game_over:
        pause = False
        title = myfont.render("Starting in :", False, YELLOW)
        for i in range(3, -1, -1):
            screen.fill(BLACK)
            screen.blit(title,
                        (width//2-title.get_width()//2,
                        height//2-title.get_height()*2)
                        )
            countdown = myfont.render(str(i), False, YELLOW)
            screen.blit(countdown, (width//2, height//2))
            pygame.display.update()
            pygame.time.delay(1000)
            
    if key[pygame.K_ESCAPE]:
        running = False

    if key[pygame.K_r]:
        (rect_mouse.x, rect_mouse.y) = start_mouse
        (rect_cat.x, rect_cat.y) = start_cat
        game_over = False
        score = 0

    pygame.display.flip()
    pygame.time.delay(delay)
pygame.quit()
