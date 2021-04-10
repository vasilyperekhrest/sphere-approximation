import math
import const
import copy

import numpy as np
import pygame as pg


class Sphere(pg.surface.Surface):
    def __init__(
            self,
            n: int = 15,
            r: int = 1,
            size: tuple[int, int] = (200, 200)
    ) -> None:
        """
        Initialization

        :param n: Number of ribs.
        :param r: Radius.
        :param size: The size of the area on which the sphere will be drawn.
        """
        pg.surface.Surface.__init__(self, size)

        self.speed = 0.02
        self.scale = 600
        self.position = (size[0]//2, size[1]//2)

        self.n = n
        self.r = r
        self.phi = math.pi / self.n
        self.delta_phi = 2 * math.pi / self.n

        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0

        self.step = 2*self.r / self.n
        self.ksi = 0
        self.delta_ksi = math.pi / self.n

        self.all_points = []
        self.__calculation()

    def __calculation(self) -> None:
        """
        Calculating the points of a sphere.
        """
        points1 = []
        points2 = []

        for i in range(self.n):
            y = self.r * math.sin(self.phi)
            x = self.r * math.cos(self.phi)
            if y > 0:
                points1.append([x, y])
            else:
                points2.append([x, y])
            self.phi += self.delta_phi

        points1.sort()
        points2.sort()

        points_down = points1[::-1] + points2
        points_up = copy.deepcopy(points_down)

        for i in range(self.n):
            points_down[i].insert(1, 0)
            points_up[i].insert(1, 0)

        points_d = copy.deepcopy(points_down)
        points_u = copy.deepcopy(points_up)

        for _ in range(self.n):
            for i in range(self.n):
                points_down[i][0] = points_d[i][0] * math.sin(self.ksi)
                points_down[i][1] = self.r * math.cos(self.ksi)
                points_down[i][2] = points_d[i][2] * math.sin(self.ksi)

                points_up[i][0] = points_u[i][0] * math.sin(self.ksi + self.delta_ksi)
                points_up[i][1] = self.r * math.cos(self.ksi + self.delta_ksi)
                points_up[i][2] = points_u[i][2] * math.sin(self.ksi + self.delta_ksi)

            self.all_points.append(copy.deepcopy(points_down + points_up))
            self.ksi += self.delta_ksi

    def update(self) -> None:
        """
        The function that will be called to redraw the points.
        """
        self.fill(color="white")
        if pg.key.get_pressed()[pg.K_DOWN]:
            self.angle_x -= self.speed
        if pg.key.get_pressed()[pg.K_UP]:
            self.angle_x += self.speed
        if pg.key.get_pressed()[pg.K_RIGHT]:
            self.angle_y -= self.speed
        if pg.key.get_pressed()[pg.K_LEFT]:
            self.angle_y += self.speed

        if pg.key.get_pressed()[pg.K_1]:
            self.angle_z += self.speed
        if pg.key.get_pressed()[pg.K_2]:
            self.angle_z -= self.speed

        rotate_x = np.array([
            [1, 0, 0],
            [0, math.cos(self.angle_x), -math.sin(self.angle_x)],
            [0, math.sin(self.angle_x), math.cos(self.angle_x)]
        ])

        rotate_y = np.array([
            [math.cos(self.angle_y), 0, -math.sin(self.angle_y)],
            [0, 1, 0],
            [math.sin(self.angle_y), 0, math.cos(self.angle_y)]
        ])

        rotate_z = np.array([
            [math.cos(self.angle_z), -math.sin(self.angle_z), 0],
            [math.sin(self.angle_z), math.cos(self.angle_z), 0],
            [0, 0, 1]
        ])

        for points in self.all_points:
            projection_points = []
            for point in points:
                point = np.dot(rotate_y, point)
                point = np.dot(rotate_x, point)
                point = np.dot(rotate_z, point)

                z = 1 / (5 - point[2])

                projection_matrix = np.array([
                    [z, 0, 0],
                    [0, z, 0]
                ])
                point = np.dot(projection_matrix, point)

                x = int(point[0] * self.scale) + self.position[0]
                y = int(point[1] * self.scale) + self.position[1]
                projection_points.append((x, y))

            self.__connect_points(projection_points)

    def __connect_points(self, points: list[tuple[int, int]]) -> None:
        """
        Function for connecting dots.

        :param points: List of points to be connected.
        """
        for i in range(self.n):
            pg.draw.line(
                self,
                const.GREEN,
                (points[i][0], points[i][1]),
                (points[(i + 1) % self.n][0], points[(i + 1) % self.n][1])
            )

            pg.draw.line(
                self,
                const.GREEN,
                (points[i + self.n][0], points[i + self.n][1]),
                (points[(i + 1) % self.n + self.n][0], points[(i + 1) % self.n + self.n][1])
            )

            pg.draw.line(
                self,
                const.GREEN,
                (points[i][0], points[i][1]),
                (points[i + self.n][0], points[i + self.n][1])
            )
