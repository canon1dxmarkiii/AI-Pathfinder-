#imports
import pygame
import math
from queue import PriorityQueue

from pygame.mixer import pause

#display
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('A* Route finding algorithm')


#colours
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255, 255, 0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64,224, 208)

class Spot:  # the main class tht deals with drawing inside the window.
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.colour == RED
    def is_open(self):
        return self.colour == GREEN
    def is_barrier(self):
        return self.colour == BLACK
    def is_start(self):
        return self.colour == ORANGE
    def is_end(self):
        return self.colour == PURPLE

    def reset(self):
        self.colour = WHITE
    def make_closed(self):
        self.colour = RED
    def make_open(self):
        self.colour = GREEN
    def make_barrier(self):
        self.colour = BLACK
    def make_end(self):
        self.colour = PURPLE
    def make_start(self):
        self.colour = ORANGE
    def make_path(self):
        self.colour = TURQUOISE
    def draw(self, win):
        pygame.draw.rect(win, self.colour,(self.x, self.y, self.width,self.width))
    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier(): # RIGHT
            self.neighbours.append(grid[self.row][self.col+1])

        if self.row > 0  and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbours.append(grid[self.row][self.col - 1])
    def __lt__(self, other):
        return False

def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def make_grid(rows, width):
    grid = []
    gap = width//rows
    for x in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(x, j, gap, rows)
            grid[x].append(spot)

    return grid

def draw_grid(win, rows, width):
    gap = width //rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win,grid,ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]: # left button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end: # drawing the start point
                    start = spot
                    start.make_start()


                elif not end and spot != start: # drawing the end point
                    end = spot
                    end.make_end()

                elif spot != start and spot != end: # drawing the barriers
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    algo(lambda: draw(win, grid, ROWS, width), grid, start, end)


def algo(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float('inf') for row in grid for spot in row}  # track of the shortest distance from start node to current node
    g_score[start] = 0
    f_score = {spot: float('inf') for row in grid for spot in row}  # track of a node to the end distance
    f_score[start] = h(start.get_pos(), end.get_pos())  # guess of distance from start to end node

    open_set_hash = {start}


main(WIN, WIDTH)