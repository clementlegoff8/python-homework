"""T1 – Snake procédural : le code de départ (étape 1).

D'après le TP « Snake » de Thierry Parmentelat et Aurélien Noce
(github.com/flotpython/exos-python), réécrit pour le cours AP Python.

Lancez-le avec :  uv run snake.py
Testez-le avec :  uv run pytest
"""

from random import randint

import pygame as pg

# Le plateau : X × Y cases de W × H pixels (étape 3).
X, Y = 30, 30
W, H = 20, 20

UP, DOWN, LEFT, RIGHT = (0, -1), (0, +1), (-1, 0), (+1, 0)


# --- logique du jeu : aucune fonction ici ne dessine -------------------------
# Ces fonctions sont vérifiées par les tests (tests/test_snake.py) :
# gardez leur nom et leurs paramètres.


def in_scope(tile):
    """Vrai si la case `tile` = (x, y) est sur le plateau."""
    return 0 <= tile[0] <= 29 and 0 <= tile[1] <= 29


def next_head(snake, direction):
    """La case où arrive la tête (le dernier élément de `snake`)."""
    x,y = snake[-1]
    i,j = direction
    return (x+i,y+j)


def turn(direction, key):
    """La nouvelle direction après l'appui sur la touche `key` (ex. pg.K_UP)."""
    if key == pg.K_UP and direction != DOWN:
        return UP
    elif key == pg.K_DOWN and direction != UP:
        return DOWN
    elif key == pg.K_LEFT and direction != RIGHT:
        return LEFT
    elif key == pg.K_RIGHT and direction != LEFT:
        return RIGHT
    else:
        return direction


def move(snake, direction, fruit):
    """Avance le serpent d'une case, en modifiant la liste `snake` sur place.

    Renvoie ce qui s'est passé : "ate", "moved", "self-bite" ou "out-of-board".
    """
    snake.append(next_head(snake,direction))
    if snake[-1] == fruit:
        return "ate"
    else:
        snake.pop(0)
        return "moved"


def random_fruit(snake):
    """Une case libre du plateau, tirée au hasard."""
    x,y = randint(0,19), randint(0,19)
    while (x,y) in snake:
        x,y = randint(0,19), randint(0,19)
    return (x,y)


# --- la boucle de jeu --------------------------------------------------------

def main():
    pg.init()
    screen = pg.display.set_mode((600, 600))
    clock = pg.time.Clock()
    snake = [(10, 15), (11, 15), (12, 15)]
    direction = RIGHT
    fruit = (randint(0,19), randint(0,19))

    running = True

    while running:
        #print("tour")
        # au plus 1 image par seconde
        clock.tick(6)

        # 1. les événements : il faut les lire, sinon la fenêtre ne répond pas
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q):
                running = False
            if event.type == pg.KEYDOWN:
                direction = turn(direction,event.key)

        # 2. l'état (rien pour l'instant)
        if move(snake,direction,fruit) == "ate":
            fruit = random_fruit(snake)

        # 3. l'affichage : on prépare l'image en mémoire...
        screen.fill((255,255,255))
        for i in range(15):
            for j in range(15):
                rect1 = pg.Rect(20+i*40,j*40,20,20)
                rect2 = pg.Rect(i*40,20+j*40,20,20)
                pg.draw.rect(screen, (200,200,200), rect1)
                pg.draw.rect(screen, (200,200,200), rect2)
        for case in snake:
            i,j = case
            rect = pg.Rect(20*i,20*j,20,20)
            pg.draw.rect(screen, (0,128,0), rect)
        rectfruit = pg.Rect(20*fruit[0],20*fruit[1],20,20)
        pg.draw.rect(screen, (255,0,0), rectfruit)

        #screen.fill((randint(0, 255), randint(0, 255), randint(0, 255)))
        # ... puis on l'envoie à l'écran, une seule fois par tour de boucle
        pg.display.update()
        
    pg.quit()

# Ce bloc ne s'exécute que si l'on lance ce fichier (uv run snake.py),
# pas quand un autre fichier fait `import snake` (les tests, par ex.).
if __name__ == "__main__":
    main()
