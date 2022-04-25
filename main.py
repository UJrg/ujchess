#!/usr/bin/env python
# -*- coding: utf-8 -*-
from legal_moves import *
import sys
import winsound
sys.setrecursionlimit(100000000)


class Game:
    def __init__(self, data, ax):
        self.data = data
        self.pickedpiece = None
        self.turn = 'W'
        self.a = 1
        self.ax = ax
        self.bol = True
        self.patch = patches.Rectangle((0, 0), 0, 0)
        self.ax.add_patch(self.patch)

    def onclick1(self, event):
        if self.a == 1:
            self.pickedpiece = cell_cords(event.xdata, event.ydata)
            if (self.pickedpiece not in self.data.position or self.data.position[self.pickedpiece][0] != self.turn)\
                    or not has_legal_move(cell_cords(event.xdata, event.ydata), self.data.position):
                winsound.PlaySound('beep-03.wav',
                                   winsound.SND_FILENAME)
            else:
                self.pointer(event, False)
                self.pointer(event, True)
                self.a = 0
        else:
            plt.title('')
            if lm(self.pickedpiece, cell_cords(event.xdata, event.ydata), self.data.position) and\
                    not king_will_in_danger(self.pickedpiece, cell_cords(event.xdata, event.ydata), self.data.position):
                if self.turn == 'W':
                    self.turn = 'B'
                else:
                    self.turn = 'W'
                winsound.PlaySound('button-46.wav', winsound.SND_FILENAME)
                self.make_castle_info(event)
                self.do_current_move(event)
            else:
                if is_castle(self.pickedpiece, cell_cords(event.xdata, event.ydata), self.data.position,
                             self.data.castle_info):
                    if self.turn == 'W':
                        self.turn = 'B'
                    else:
                        self.turn = 'W'
                    winsound.PlaySound('button-46.wav', winsound.SND_FILENAME)
                    self.make_castle_info(event)
                    self.do_castling(event)
        plt.show()

    def get_result(self):
        if self.turn == 'W':
            plt.title('Blacks Won', color=mes_col)
        else:
            plt.title('Whites Won', color=mes_col)


    def do_current_move(self, event):
        image = plt.imread(self.data.position[self.pickedpiece] + '.png')
        if cell_cords(event.xdata, event.ydata) in self.data.position:
            self.data.pos_img[cell_cords(event.xdata, event.ydata)].remove()
        self.data.position[cell_cords(event.xdata, event.ydata)] = self.data.position[self.pickedpiece]
        del self.data.position[self.pickedpiece]
        imgplot = plt.imshow(image, extent=cords_cords(event.xdata, event.ydata), zorder=2)
        self.data.pos_img[cell_cords(event.xdata, event.ydata)] = imgplot
        self.data.pos_img[self.pickedpiece].remove()
        self.create_new_queen(event)
        if king_in_danger(self.turn, self.data.position):
            plt.title('Check', color=mes_col)
            if is_mate(self.turn, self.data.position):
                self.get_result()
                plt.show()
        self.a = 1
        plt.show()

    def do_castling(self, event):
        image = plt.imread(self.data.position[self.pickedpiece] + '.png')
        if self.pickedpiece in self.data.pos_img:
            self.data.pos_img[self.pickedpiece].remove()
        self.data.position[cell_cords(event.xdata, event.ydata)] = self.data.position[self.pickedpiece]
        del self.data.position[self.pickedpiece]
        imgplot = plt.imshow(image, extent=cords_cords(event.xdata, event.ydata), zorder=2)
        self.data.pos_img[cell_cords(event.xdata, event.ydata)] = imgplot
        cell = cell_cords(event.xdata, event.ydata)
        self.make_rook_move(cell)
        if king_in_danger(self.turn, self.data.position):
            plt.title('Check', color=mes_col)
            if is_mate(self.turn, self.data.position):
                self.get_result()
                plt.show()
        self.a = 1
        plt.show()

# ეს მეთოდი გამოიძახება როქის დროს ტურის სვლის გასაკეთებლად და შესაბამისი ინფორმაციის ჩასაწერად.
    def make_rook_move(self, cell):
        cell1 = None
        cell2 = None
        if cell == 'c8':
            cell1 = 'a8'
            cell2 = 'd8'
        if cell == 'g8':
            cell1 = 'h8'
            cell2 = 'f8'
        if cell == 'c1':
            cell1 = 'a1'
            cell2 = 'd1'
        if cell == 'g1':
            cell1 = 'h1'
            cell2 = 'f1'
        image = plt.imread(self.data.position[cell1] + '.png')
        self.data.position[cell2] = self.data.position[cell1]
        if cell1 in self.data.pos_img:
            self.data.pos_img[cell1].remove()
        del self.data.position[cell1]
        imgplot = plt.imshow(image, extent=cords_cell(cell2), zorder=2)
        self.data.pos_img[cell2] = imgplot

    def make_castle_info(self, event):
        if self.pickedpiece == 'a8' or cell_cords(event.xdata, event.ydata) == 'a8':
            self.data.castle_info.append('c8')
        if self.pickedpiece == 'e8' or cell_cords(event.xdata, event.ydata) == 'e8':
            self.data.castle_info.append('e8')
        if self.pickedpiece == 'h8' or cell_cords(event.xdata, event.ydata) == 'h8':
            self.data.castle_info.append('g8')
        if self.pickedpiece == 'a1' or cell_cords(event.xdata, event.ydata) == 'a1':
            self.data.castle_info.append('c1')
        if self.pickedpiece == 'e1' or cell_cords(event.xdata, event.ydata) == 'e1':
            self.data.castle_info.append('e1')
        if self.pickedpiece == 'h1' or cell_cords(event.xdata, event.ydata) == 'h1':
            self.data.castle_info.append('g1')


    def create_new_queen(self, event):
        if cell_cords(event.xdata, event.ydata)[1] == '8' and\
           self.data.position[cell_cords(event.xdata, event.ydata)] == 'WP':
            image = plt.imread('WQ.png')
            self.data.pos_img[cell_cords(event.xdata, event.ydata)].remove()
            self.data.position[cell_cords(event.xdata, event.ydata)] = 'WQ'
            imgplot = plt.imshow(image, extent=cords_cords(event.xdata, event.ydata), zorder=2)
            self.data.pos_img[cell_cords(event.xdata, event.ydata)] = imgplot
        if cell_cords(event.xdata, event.ydata)[1] == '1' and\
           self.data.position[cell_cords(event.xdata, event.ydata)] == 'BP':
            image = plt.imread('BQ.png')
            self.data.pos_img[cell_cords(event.xdata, event.ydata)].remove()
            self.data.position[cell_cords(event.xdata, event.ydata)] = 'BQ'
            imgplot = plt.imshow(image, extent=cords_cords(event.xdata, event.ydata), zorder=2)
            self.data.pos_img[cell_cords(event.xdata, event.ydata)] = imgplot

    def pointer(self, event, bol):
        if bol:
            self.patch = patches.Rectangle((cords_cords(event.xdata, event.ydata)[0],
                                            cords_cords(event.xdata, event.ydata)[2]), size, size)
            self.patch.set_color(pointer_col)
            self.ax.add_patch(self.patch)
        else:
            self.patch.remove()


def letsplay():
    plt.delaxes()
    ax = create_axis()
    data = Data()
    game = Game(data, ax)
    draw_desk(ax)
    annotate(ax)
    data.daxatva()
    fig.canvas.mpl_connect('button_press_event', game.onclick1)
    plt.show()


letsplay()
plt.show()
