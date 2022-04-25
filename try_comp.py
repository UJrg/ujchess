#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import sys
from comp_moves import *
sys.setrecursionlimit(100000000)

class Game_C:
    def __init__(self, data, ax):
        self.ax = ax
        self.data = data
        self.turn = 1
        self.a = 1
        self.pickedpiece = None

    def onclick(self, event):
        if self.turn == 1:
            if self.a == 1:
                self.pickedpiece = cell_cords(event.xdata, event.ydata)
                if (self.pickedpiece not in self.data.position or self.data.position[self.pickedpiece][0] != 'W')\
                        or not has_legal_move(cell_cords(event.xdata, event.ydata), self.data.position):
                    pass
                else:
                    self.a = 0
            else:
                if lm(self.pickedpiece, cell_cords(event.xdata, event.ydata), self.data.position) and \
                        not king_will_in_danger(self.pickedpiece, cell_cords(event.xdata, event.ydata),
                                                self.data.position):
                    self.a = 1
                    self.turn = 0
                    self.do_human_move(event)
                    plt.show()
        else:
            self.turn = 1
            self.do_computer_move()
            plt.show()

    def do_human_move(self, event):
        image = plt.imread(self.data.position[self.pickedpiece] + '.png')
        if cell_cords(event.xdata, event.ydata) in self.data.position:
            self.data.pos_img[cell_cords(event.xdata, event.ydata)].remove()
        self.data.position[cell_cords(event.xdata, event.ydata)] = self.data.position[self.pickedpiece]
        del self.data.position[self.pickedpiece]
        imgplot = plt.imshow(image, extent=cords_cords(event.xdata, event.ydata), zorder=2)
        self.data.pos_img[cell_cords(event.xdata, event.ydata)] = imgplot
        self.data.pos_img[self.pickedpiece].remove()
        self.create_new_queen([self.pickedpiece, cell_cords(event.xdata, event.ydata)])
        plt.show()

    def do_computer_move(self):
        lis = every_legal_move('B', self.data.position)
        lis1 = optimize_lis(lis, self.data.position)
        if len(lis1) == 0:
            plt.title('whites won', color=mes_col)
        else:
            a = random.choice(lis1)
            image = plt.imread(self.data.position[a[0]] + '.png')
            if a[1] in self.data.position:
                self.data.pos_img[a[1]].remove()
            self.data.position[a[1]] = self.data.position[a[0]]
            del self.data.position[a[0]]
            imgplot = plt.imshow(image, extent=cords_cell(a[1]), zorder=2)
            self.data.pos_img[a[1]] = imgplot
            self.data.pos_img[a[0]].remove()
            self.create_new_queen(a)
            plt.show()

    def create_new_queen(self, move):
        if move[1][1] == '8' and \
                self.data.position[move[1]] == 'WP':
            image = plt.imread('WQ.png')
            self.data.pos_img[move[1]].remove()
            self.data.position[move[1]] = 'WQ'
            imgplot = plt.imshow(image, extent=cords_cell(move[1]), zorder=2)
            self.data.pos_img[move[1]] = imgplot
        if move[1][1] == '1' and \
                self.data.position[move[1]] == 'BP':
            image = plt.imread('BQ.png')
            self.data.pos_img[move[1]].remove()
            self.data.position[move[1]] = 'BQ'
            imgplot = plt.imshow(image, extent=cords_cell(move[1]), zorder=2)
            self.data.pos_img[move[1]] = imgplot


def letsplay():
    plt.delaxes()
    ax = create_axis()
    data = Data()
    game = Game_C(data, ax)
    draw_desk(ax)
    annotate(ax)
    data.daxatva()
    fig.canvas.mpl_connect('button_press_event', game.onclick)
    plt.show()


letsplay()
plt.show()
