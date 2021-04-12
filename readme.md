---
title: Le chat et la souris
---

![Chat-Souris](exemple_collision.png)


# Introduction

`PyGame` utilise des objets de type `Surface`. Par exemple
la documentation de `pygame.image.load()` nous indique:

~~~
load new image from a file (or file-like object)
load(filename) -> Surface
load(fileobj, namehint="") -> Surface
~~~

La méthode `pygame.image.load()` prend en paramètre le nom du fichier
image (filename) est renvoie un objet de type `Surface`.

De même la documentation de la méthode `pygame.display.set_mode()` donne

~~~
Initialize a window or screen for display
set_mode(size=(0, 0), flags=0, depth=0, display=0, vsync=0) -> Surface
~~~

Ainsi les objets de type `Surface` possède par exemple les méthodes:

- `pygame.Surface.blit` : draw one image onto another
- `pygame.Surface.fill` : fill Surface with a solid color
- `pygame.Surface.subsurface` : create a new surface that references its parent
- `pygame.Surface.get_size` : get the dimensions of the Surface
- `pygame.Surface.get_width` : get the width of the Surface
- `pygame.Surface.get_height` : get the height of the Surface
- `pygame.Surface.get_rect` : get the rectangular area of the Surface
- ...

Ici c'est la méthode `pygame.Surface.blit` qui nous intéresse. La documentation
indique :

~~~
draw one image onto another
blit(source, dest, area=None, special_flags=0) -> Rect
~~~

avec : `The dest argument can either be a pair of coordinates 
representing the position of the upper left corner of the blit or a Rect, 
where the upper left corner of the rectangle will be used as the position 
for the blit.`

Exemple de code:

~~~python
...
screen = pygame.display.set_mode((600, 600)) # screen est de type Surface
img_cat = pygame.image.load('cat.png') # idem
screen.blit(img_cat, (300, 300)) # dessine l'image au "centre" de l'écran
...
~~~

1. ![Q] Expliquer pourquoi dans les commentaires centre est entre double quotes.
    on utilise 300 au lieu de width//2, le centre ne s'adaptera pas si on change la taille de la fenetre.


# Coordonnées d'un rectangle

Les objets de type `Rect` possèdent des attributs "virtuelles" : 

~~~
x,y
top, left, bottom, right
topleft, bottomleft, topright, bottomright
midtop, midleft, midbottom, midright
center, centerx, centery
size, width, height
w,h
~~~

Ci-dessous un exemple de code illustrant ces attributs :

~~~python
#!/bin/python3

"inspiré de : https://pygame.readthedocs.io/en/latest/rect/rect.html#virtual-attributes"

import pygame

width = 500
height = 200
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((width, height))
font = pygame.font.Font(None, 24)
running = True

def draw_point(text, pos):
    img = font.render(text, True, BLACK)
    pygame.draw.circle(screen, RED, pos, 3)
    screen.blit(img, pos)

rect = pygame.Rect(50, 40, 250, 80)
pts = ('topleft', 'topright', 'bottomleft', 'bottomright',
        'midtop', 'midright', 'midbottom', 'midleft', 'center')

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(GRAY)
    pygame.draw.rect(screen, GREEN, rect, 4)

    for pt in pts:
        draw_point(pt, eval('rect.'+pt))

    pygame.display.flip()
    pygame.time.delay(50)
pygame.quit()
~~~

Ces attributs peuvent être utilisés comme mutateur. Exemple:

~~~python
...
screen = pygame.display.set_mode((600, 600)) 
img_cat = pygame.image.load('cat.png')
rect_cat = img_cat.get_rect()
(w, h) = screen.get_size()
rect_cat.center = (w//2, h//2)
screen.blit(img_cat, rect_cat) # dessine le centre de l'image au centre de l'écran
...
~~~

# Version 1

## Les images
Réaliser une première version avec les contraintes suivantes:

- Une image libre de droit de fond
- Une image libre de droit de souris au centre
- Une image libre de droit de chat en haut a gauche

(Si besoin utilisé `pygame.transform.scale` pour redimensionner l'image)

## Déplacement du chat

1. ![Q] En reprenant le travail sur le pong, déplacer le chat à l'aide des touches
de direction. (ne pas se préoccuper des collisions)

# Détection de collision

Une collision se produit lorsque deux objets rentre en contact. L'objet 
`Rect` possède quelques méthodes permettant de faciliter la gestion
de collision :

- `collidepoint((x,y)) -> bool` : test if a point is inside a rectangle
- `colliderect(Rect) -> bool` : test if a point is inside a rectangle
- `colliderect(list) -> index` : test if one rectangle in a list intersects
- ...

## Collision entre le chat est la souris

Si on détecte une collision entre le chat et la souris on :

- Dessine un rectangle bleu autour du chat
- Dessine un rectangle vert autour de la souris
- Dessine un rectangle rouge dans la zone de collision


Exemple:

~~~python
if rect_cat.colliderect(rect_mouse):
    pygame.draw.rect(screen, GREEN, rect_mouse)
    pygame.draw.rect(screen, BLUE, rect_cat)
    rect_clip = rect_cat.clip(rect_mouse)
    pygame.draw.rect(screen, RED, rect_clip)
screen.blit(img_mouse, rect_mouse)
screen.blit(img_cat, rect_cat)
~~~

1. ![Q] Réaliser le programme utilisant le code précédent

## Détection des bordures de l'écran

Pour détecter que le chat ne sort pas de l'écran on peux donc définir
par exemple :

- `bord_haut = pygame.Rect(0, -1, width, 1)`
- `bord_bas = pygame.Rect(0, height, width, 1)`

Il suffit alors de déclarer une liste des bords :

~~~python
bords = [bord_haut, bord_bas]
~~~

et d'utiliser le test suivant :

~~~python
if rect_cat.collidelist(bord) != -1:
    # Collision
~~~

1. ![Q] Quels sont les paramètres de pygame.Rect ?

Lors du déplacement du chat implémenter l'algorithme suivant:

- Mémoriser la position courante du chat
- Déplacer le chat
- Si collision, remettre le chat à sa position précédente

Exemple :

~~~python
mem = (rect_cat.x, rect_cat.y)
rect_cat = rect_cat.move(directions[direction])
if rect_cat.collidelist(bords) != -1:
    (rect_cat.x, rect_cat.y) = mem
~~~

2. ![Q] Implémenter la détection des bords haut et bas
2. ![Q] Modifier le code pour détecter les bords gauche et droit

# Faire un jeu

1. ![Q] Je vous laisse le soin d'imaginer un jeu.

[Q]: gears.png
