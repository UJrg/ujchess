#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.patches as patches

lims = 2500
factor = 12.5
size = lims/factor
back_col = 'black'
cell_col = 'red'
pointer_col = 'green'
mes_col = 'white'
fig = plt.figure(facecolor=back_col)


def create_axis():
    ax = fig.add_subplot(111)
    ax.set_facecolor(back_col)
    plt.xticks([])
    plt.yticks([])
    ax.set_xlim(0, lims)
    ax.set_ylim(0, lims)
    return ax


def annotate(ax):
    for m in range(8):
        ax.annotate(letters[m], xy = (2,1), xytext=((lims-8*size)/2+m*size+size/3, (lims-8*size)/2-size/2), color = 'white')
        ax.annotate(digits[m], xy = (2,1), xytext=((lims-8*size)/2-size/2, (lims-8*size)/2+m*size+size/3), color = 'white')

digits = ['1', '2', '3', '4', '5', '6', '7', '8']
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
pieces = ['WP', 'WR', 'WN', 'WB', 'WK', 'WQ', 'BP', 'BR', 'BN', 'BB', 'BQ', 'BK']
chessboard = [[0 for x in range(8)] for y in range(8)]

for i in range(8):
    for j in range(8):
        chessboard[i][j] = letters[i]+digits[j]

class Data:
    def __init__(self):
        self.position = {'a8': 'BR', 'b8': 'BN', 'c8': 'BB', 'd8': 'BQ', 'e8': 'BK', 'f8': 'BB', 'g8': 'BN', 'h8': 'BR',
                         'a7': 'BP', 'b7': 'BP', 'c7': 'BP', 'd7': 'BP', 'e7': 'BP', 'f7': 'BP', 'g7': 'BP', 'h7': 'BP',
                         'a1': 'WR', 'b1': 'WN', 'c1': 'WB', 'd1': 'WQ', 'e1': 'WK', 'f1': 'WB', 'g1': 'WN', 'h1': 'WR',
                         'a2': 'WP', 'b2': 'WP', 'c2': 'WP', 'd2': 'WP', 'e2': 'WP', 'f2': 'WP', 'g2': 'WP', 'h2': 'WP'}
        self.pos_img = {}
        self.castle_info = []

    def daxatva(self):
        for m in range(8):
            for n in range(8):
                if chessboard[m][n] in self.position:
                    image = plt.imread(self.position[chessboard[m][n]] + '.png')
                    imgplot = plt.imshow(image, extent=cords_cell(chessboard[m][n]), zorder=1)
                    self.pos_img[chessboard[m][n]] = imgplot


def draw_desk(ax):
    for m in range(8):
        for n in range(8):
            patch = patches.Rectangle(((lims-8*size)/2+size*m, (lims-8*size)/2+size*n), size, size, zorder=0)
            if (m+n) % 2 == 0:
                patch.set_color(cell_col)
            else:
                patch.set_color('beige')
            ax.add_patch(patch)
    pass


def cell_cords(x_cor, y_cor):
    for m in range(8):
        for n in range(8):
            if (lims-8*size)/2+(m+1)*size > x_cor > (lims-8*size)/2+m*size and \
                    (lims - 8 * size) / 2 + (n + 1) * size > y_cor > (lims-8*size)/2+n*size:
                return chessboard[m][n]
    pass


def cords_cords(x_cor, y_cor):
    for m in range(8):
        for n in range(8):
            if (lims-8*size)/2+(m+1)*size > x_cor > (lims-8*size)/2+m*size and \
                    (lims - 8 * size) / 2 + (n + 1) * size > y_cor > (lims-8*size)/2+n*size:
                return [(lims-8*size)/2+m*size, (lims-8*size)/2+(m+1)*size,
                        (lims-8*size)/2+n*size, (lims-8*size)/2+(n+1)*size]
    pass


def cords_cell(cell):
    for m in range(8):
        for n in range(8):
            if chessboard[m][n] == cell:
                return [(lims-8*size)/2+m*size, (lims-8*size)/2+(m+1)*size,
                        (lims-8*size)/2+n*size, (lims-8*size)/2+(n+1)*size]
    pass
