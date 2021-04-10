import pygame as pg
import const
from sphere import Sphere


def main() -> None:
    pg.init()
    pg.display.set_caption("Sphere")
    screen = pg.display.set_mode((const.WIDTH, const.HEIGHT))
    screen.fill(const.WHITE)
    clock = pg.time.Clock()

    sphere = Sphere(size=(const.WIDTH, const.HEIGHT))

    running = True
    while running:
        screen.fill(const.WHITE)
        clock.tick(const.FPS)

        screen.blit(sphere, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        sphere.update()
        pg.display.flip()


if __name__ == "__main__":
    main()
