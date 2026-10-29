"""T2 – Boids : le code de départ (étape 0).

D'après le TP « boids » de Thierry Parmentelat (flotpython), réécrit pour le
cours AP Python et pour arcade 3.

Lancez-le avec :  uv run boids.py
Testez-le avec :  uv run pytest
"""

import math  # (servira à l'étape 2)
import random  # (servira à l'étape 4)
from pathlib import Path

import arcade

WIDTH, HEIGHT = 800, 800
BACKGROUND = arcade.color.ALMOND

# Les images, cherchées à côté de ce fichier, d'où qu'on le lance.
HERE = Path(__file__).parent
ARROW = HERE / "media" / "arrow.png"
OBSTACLE = HERE / "media" / "obstacle.png"
SKY = HERE / "media" / "sky.png"  # le décor (étape 9)
SKY2 = HERE / "media" / "sky2.png"

SPEED = 100  # pixels par seconde (étape 2)
TURN_SPEED = 180  # degrés par seconde, tant qu'une flèche est enfoncée (étape 5)
NOISE = 3  # écart maximal du cap à chaque mise à jour, en degrés (étape 5)
N_BOIDS = 20  # (étape 4)
GRID = 10  # GRID × GRID obstacles (étape 6)
RADIUS = 30  # rayon de détection des voisins, en pixels (étapes 7 et 8)


# --- les objets du jeu -------------------------------------------------------
# Ces classes et fonctions sont vérifiées par les tests (tests/test_boids.py) :
# gardez leur nom et leurs paramètres.
#
# Chaque `raise NotImplementedError("étape …")` est un trou à remplir. S'il est
# atteint, le programme s'arrête net, avec ce message : il dit à quelle étape
# écrire ce morceau. Quand vous y arrivez, effacez la ligne et écrivez votre code.
# À l'étape 0, la fenêtre n'utilise encore aucune de ces classes : rien ne casse.


class Boid(arcade.Sprite):
    """Un oiseau : une flèche qui avance dans la direction où elle pointe."""

    def __init__(self, x, y, angle, speed=SPEED, turning=0, others=None):
        super().__init__(ARROW, center_x=x, center_y=y, angle=angle)
        self.speed = speed
        self.turning = turning
        self.others = others

    def update(self, delta_time=1 / 60, *args, **kwargs):
        """Appelée par arcade (via la SpriteList) à chaque mise à jour."""
        rad = math.radians(self.angle)
        self.center_x += self.speed * delta_time * math.cos(rad)
        self.center_y -= self.speed * delta_time * math.sin(rad)
        self.center_x = self.center_x % WIDTH
        self.center_y = self.center_y % HEIGHT
        self.angle += self.turning * TURN_SPEED * delta_time
        self.angle += random.uniform(-NOISE,NOISE)
        if self.others != None:
            self.center_x += self.separation(self.others)[0]
            self.center_y += self.separation(self.others)[1]
            if len(self.neighbours(self.others)) > 0:
                self.alpha = 128
            else:
                self.alpha = 255

    def neighbours(self, others, radius=RADIUS):
        """Les objets de `others` à moins de `radius` pixels, sauf soi-même."""
        neighbours = []
        for other in others:
            if math.dist(self.position, other.position) < radius and other != self:
                neighbours.append(other)
        return neighbours

    def separation(self, others, radius=RADIUS):
        """Le déplacement (dx, dy) qui écarte le boid de ses voisins."""
        dx,dy = 0,0
        for other in self.neighbours(others):
            d = math.dist(self.position, other.position)
            dx += (self.center_x - other.center_x)*(1-d/radius)/2
            dy += (self.center_y - other.center_y)*(1-d/radius)/2
        return (dx,dy)


class Obstacle(arcade.Sprite):
    """Un obstacle immobile."""
    def __init__(self, x, y):
        super().__init__(OBSTACLE, center_x=x, center_y=y)


def random_boids(n, others=None):
    """n boids placés et orientés au hasard, qui évitent tous `others`."""
    boids = arcade.SpriteList()
    for i in range(n):
        x,y,a = random.uniform(0,800), random.uniform(0,800), random.uniform(0,360)
        boid = Boid(x,y,a,others=others)
        boids.append(boid)
    return boids


def obstacle_grid(n):
    """n × n obstacles régulièrement espacés, au centre de leur carré."""
    obstacles = arcade.SpriteList()
    pas_horizontal = WIDTH / n
    pas_vertical = HEIGHT / n
    for i in range(n):
        for j in range(n):
            obstacles.append(Obstacle(pas_horizontal * (i + 1/2), pas_vertical * (j + 1/2)))
    return obstacles


# --- la fenêtre ---------------------------------------------------------------


class MyWindow(arcade.Window):
    def __init__(self):
        # d'abord, ce que fait toute fenêtre d'arcade : s'ouvrir, en WIDTH × HEIGHT
        # pixels, avec « Boids » pour titre (super() : on y revient en séance)
        super().__init__(WIDTH, HEIGHT, "Boids")
        self.background_color = BACKGROUND  # la couleur que self.clear() étale

        # une SpriteList : une liste de sprites, qu'arcade dessine d'un coup
        self.boids = arcade.SpriteList()
        self.others = arcade.SpriteList()
        self.sky = arcade.SpriteList()
        self.sky.append(arcade.Sprite(SKY2, center_x = WIDTH/2, center_y = HEIGHT/2))
        self.boids.extend(random_boids(N_BOIDS,self.others))
        self.others.extend(self.boids)
        self.others.extend(obstacle_grid(GRID))

    def on_update(self, delta_time):
        self.boids.update(delta_time)

    def on_draw(self):
        self.clear()
        self.sky.draw()
        obstacle_grid(GRID).draw()
        self.boids.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            for boid in self.boids:
                boid.turning = -1
        elif symbol == arcade.key.RIGHT:
            for boid in self.boids:
                boid.turning = 1
        elif symbol == arcade.key.Q:
            self.close()

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            for boid in self.boids:
                boid.turning = 0

def main():
    MyWindow()
    arcade.run()


# Ce bloc ne s'exécute que si l'on lance ce fichier (uv run boids.py),
# pas quand un autre fichier fait `import boids` (les tests, par ex.).
if __name__ == "__main__":
    main()
