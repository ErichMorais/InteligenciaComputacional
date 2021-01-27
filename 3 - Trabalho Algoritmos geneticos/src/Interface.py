
import turtle
import time
from Constants import WALL
from Population import *

matrix = [
    "WWWWWWIW",
    "W      W",
    "W   W WW",
    "W WWW  W",
    "W      W",
    "W  WWW W",
    "W      W",
    "WFWWWWWW"
]


class Wall(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)


class Final(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("red")
        self.penup()
        self.speed(0)


class Child(turtle.Turtle):
    def __init__(self, square_size):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("green")
        self.penup()
        self.speed(0)
        self.limit = square_size

    def move_to_east(self):
        self.goto(self.xcor() + self.limit, self.ycor())
        return

    def move_to_west(self):
        self.goto(self.xcor() - self.limit, self.ycor())
        return

    def move_to_south(self):
        self.goto(self.xcor(), self.ycor() + self.limit)
        return

    def move_to_north(self):
        self.goto(self.xcor(), self.ycor() - self.limit)
        return

    def move_to_init(self, init):
        l_i, c_i = init.split(',')
        l_i = int(l_i)
        c_i = int(c_i)
        self.goto(l_i, c_i)
        time.sleep(0.2)
        return

    def move(self, way, screenAG, mov_quantify):

        move = 0

        for t in range(mov_quantify):

            move = way & 0b000000000000000000000011  # Seprar os bits menos significativos
            way = way >> 2

            if move == 0:
                self.move_to_east()
            elif move == 1:
                self.move_to_north()
            elif move == 2:
                self.move_to_west()
            elif move == 3:
                self.move_to_south()

            time.sleep(0.01)
            screenAG.update()

        return


def CreateMatrix(matrix, wall, child, final, square_size):
    objective_point = []; wall_exist = []

    for l in range(len(matrix)):
        for c in range(len(matrix[l])):
            matrix_pos = matrix[l][c]
            screen_x = -90 + (l*square_size)
            screen_y = 90 - (c*square_size)

            if (matrix_pos == "I"):
                child.goto(screen_x, screen_y)
                objective_point.append(f'{screen_x},{screen_y}')

            if (matrix_pos == "F"):
                final.goto(screen_x, screen_y)
                final.stamp()
                objective_point.append(f'{screen_x},{screen_y}')

            if (matrix_pos == "W"):
                wall.goto(screen_x, screen_y)
                wall.stamp()
                wall_exist.append(f'{screen_x},{screen_y}')

    return wall_exist, objective_point


def locateWalls(matrix_clean, walls, aim_p):
    objective = []
    matrix_est = np.ones(matrix_clean.shape)
    Line, Column = matrix_est.shape

    y_min1, y_min2 = walls[0].split(',')
    y_max1, y_max2 = walls[(len(walls) - 1)].split(',')

    m1, b1 = getCoefs(int(y_min1), int(y_min2), Line-1, 0)
    m2, b2 = getCoefs(int(y_max1), int(y_max2), Column-1, 0)

    for i in range(len(walls)):
        y, x = walls[i].split(',')
        y = int(y)
        x = int(x)

        l = int(round((y - b1)/m1))
        c = int(round((x - b2)/m2))

        if(l < Line and c >= 0 and c < Column and l >= 0):
            matrix_est[l][c] = WALL

    for i in range(2):
        y, x = aim_p[i].split(',')
        y = int(y)
        x = int(x)

        l = int(round((y - b1)/m1))
        c = int(round((x - b2)/m2))

        if(l < Line and c >= 0 and c < Column and l >= 0):
            matrix_est[l][c] = 0
            objective.append(f'{l},{c}')

    return matrix_est, objective


def getCoefs(min_Y, max_Y, max_X, min_X):

    first = {'x': max_X, 'y': max_Y}
    second = {'x': min_X, 'y': min_Y}

    m = int(second['y'] - first['y']) / (second['x'] - first['x'])
    b = first['y'] - m*first['x']

    return m, b
