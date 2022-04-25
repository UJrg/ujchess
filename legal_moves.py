#!/usr/bin/env python
# -*- coding: utf-8 -*-
from data import *

def indexof(cell):
    for m in range(8):
        for n in range(8):
            if chessboard[m][n] == cell:
                return m, n


def lm(cell1, cell2, pos):
    if cell1 not in pos:
        return False
    else:
        piece = pos[cell1]
    if piece[1] == 'P':
        return is_plm(cell1, cell2, pos)
    elif piece[1] == 'R':
        return is_rlm(cell1, cell2, pos)
    elif piece[1] == 'N':
        return is_nlm(cell1, cell2, pos)
    elif piece[1] == 'B':
        return is_blm(cell1, cell2, pos)
    elif piece[1] == 'K':
        return is_klm(cell1, cell2, pos)
    elif piece[1] == 'Q':
        return is_qlm(cell1, cell2, pos)


def is_plm(cell1, cell2, pos):
    if pos[cell1][0] == 'B' and indexof(cell1)[0] == indexof(cell2)[0] and (
            indexof(cell1)[1] - 1 == indexof(cell2)[1] or
            indexof(cell1)[1] - 2 == indexof(cell2)[1] and cell1[1] == '7') and cell2 not in pos:
        return True
    elif pos[cell1][0] == 'W' and indexof(cell1)[0] == indexof(cell2)[0] and (indexof(cell1)[1] + 1 == indexof(cell2)[1]
                                                                              or indexof(cell1)[1] + 2 ==
                                                                              indexof(cell2)[1] and cell1[
                                                                                  1] == '2') and cell2 not in pos:
        return True
    elif pos[cell1][0] == 'B' and (
            indexof(cell1)[0] + 1 == indexof(cell2)[0] or indexof(cell1)[0] - 1 == indexof(cell2)[0]) \
            and indexof(cell1)[1] - 1 == indexof(cell2)[1] and cell2 in pos and pos[cell2][0] == 'W':
        return True
    elif pos[cell1][0] == 'W' and (
            indexof(cell1)[0] + 1 == indexof(cell2)[0] or indexof(cell1)[0] - 1 == indexof(cell2)[0]) \
            and indexof(cell1)[1] + 1 == indexof(cell2)[1] and cell2 in pos and pos[cell2][0] == 'B':
        return True
    return False


def is_rlm(cell1, cell2, pos):
    if cell2 in pos and pos[cell1][0] == pos[cell2][0]:
        return False
    if indexof(cell1)[0] == indexof(cell2)[0] and indexof(cell1)[1] > indexof(cell2)[1]:
        for m in range(indexof(cell2)[1] + 1, indexof(cell1)[1], 1):
            if chessboard[indexof(cell1)[0]][m] in pos:
                return False
        return True
    if indexof(cell1)[0] == indexof(cell2)[0] and indexof(cell1)[1] < indexof(cell2)[1]:
        for m in range(indexof(cell1)[1] + 1, indexof(cell2)[1], 1):
            if chessboard[indexof(cell1)[0]][m] in pos:
                return False
        return True
    if indexof(cell1)[1] == indexof(cell2)[1] and indexof(cell1)[0] > indexof(cell2)[0]:
        for m in range(indexof(cell2)[0] + 1, indexof(cell1)[0], 1):
            if chessboard[m][indexof(cell1)[1]] in pos:
                return False
        return True
    if indexof(cell1)[1] == indexof(cell2)[1] and indexof(cell1)[0] < indexof(cell2)[0]:
        for m in range(indexof(cell1)[0] + 1, indexof(cell2)[0], 1):
            if chessboard[m][indexof(cell1)[1]] in pos:
                return False
        return True
    return False


def is_blm(cell1, cell2, pos):
    dx = indexof(cell2)[1] - indexof(cell1)[1]
    dy = indexof(cell2)[0] - indexof(cell1)[0]
    if cell2 in pos and pos[cell1][0] == pos[cell2][0]:
        return False
    if abs(dx) != abs(dy):
        return False
    if dx == dy:
        if dx > 0:
            for m in range(1, dx, 1):
                if chessboard[indexof(cell1)[0] + m][indexof(cell1)[1] + m] in pos:
                    return False
        else:
            for m in range(1, -dx, 1):
                if chessboard[indexof(cell1)[0] - m][indexof(cell1)[1] - m] in pos:
                    return False
    else:
        if dx > 0:
            for m in range(1, dx, 1):
                if chessboard[indexof(cell1)[0] - m][indexof(cell1)[1] + m] in pos:
                    return False
        else:
            for m in range(1, -dx, 1):
                if chessboard[indexof(cell1)[0] + m][indexof(cell1)[1] - m] in pos:
                    return False
    return True


def is_qlm(cell1, cell2, pos):
    return is_rlm(cell1, cell2, pos) or is_blm(cell1, cell2, pos)


def is_nlm(cell1, cell2, pos):
    if cell2 in pos and pos[cell1][0] == pos[cell2][0]:
        return False
    if (abs(indexof(cell2)[0] - indexof(cell1)[0]) == 2 and abs(indexof(cell2)[1] - indexof(cell1)[1]) == 1) or \
            (abs(indexof(cell2)[0] - indexof(cell1)[0]) == 1 and abs(indexof(cell2)[1] - indexof(cell1)[1]) == 2):
        return True
    return False


def is_klm(cell1, cell2, pos):
    if cell2 in pos and pos[cell1][0] == pos[cell2][0]:
        return False
    if abs(indexof(cell2)[0] - indexof(cell1)[0]) ** 2 + abs(indexof(cell2)[1] - indexof(cell1)[1]) ** 2 > 2:
        return False
    return True


def king_in_danger(color, pos):
    for key in pos:
        if pos[key] == color + 'K':
            king_cell = key
            for keys in pos:
                if pos[keys][0] != color and lm(keys, king_cell, pos):
                    return True
    return False


def is_castle(cell1, cell2, pos, info):
    if cell1 != 'e1' and cell1 != 'e8':
        return False
    if king_in_danger(pos[cell1][0], pos):
        return False
    if cell1 in info or cell2 in info:
        return False
    if king_will_in_danger(cell1, cell2, pos):
        return False
    if cell1 not in pos:
        return False
    if pos[cell1] == 'BK' and indexof(cell1)[1] == indexof(cell2)[1] and indexof(cell1)[0] - 2 == indexof(cell2)[0] and \
            'a8' in pos and pos['a8'] == 'BR' and 'b8' not in pos and 'c8' not in pos and 'd8' not in pos:
        return True
    if pos[cell1] == 'BK' and indexof(cell1)[1] == indexof(cell2)[1] and indexof(cell1)[0] + 2 == indexof(cell2)[0] and \
            'h8' in pos and pos['h8'] == 'BR' and 'f8' not in pos and 'g8' not in pos:
        return True
    if pos[cell1] == 'WK' and indexof(cell1)[1] == indexof(cell2)[1] and indexof(cell1)[0] - 2 == indexof(cell2)[0] and \
            'a1' in pos and pos['a1'] == 'WR' and 'b1' not in pos and 'c1' not in pos and 'd1' not in pos:
        return True
    if pos[cell1] == 'WK' and indexof(cell1)[1] == indexof(cell2)[1] and indexof(cell1)[0] + 2 == indexof(cell2)[0] \
            and 'h1' in pos and pos['h1'] == 'WR' and 'f1' not in pos and 'g1' not in pos:
        return True
    return False


def is_mate(color, pos):
    for key in pos:
        if pos[key][0] == color:
            for m in range(8):
                for n in range(8):
                    var_pos = pos.copy()
                    if lm(key, chessboard[m][n], var_pos):
                        var_pos[chessboard[m][n]] = var_pos[key]
                        del var_pos[key]
                        if not king_in_danger(color, var_pos):
                            return False
    return True



def king_will_in_danger(cell1, cell2, pos):
    var_pos = pos.copy()
    if cell1 in var_pos:
        color = var_pos[cell1][0]
        var_pos[cell2] = var_pos[cell1]
        del var_pos[cell1]
        if king_in_danger(color, var_pos):
            return True
    return False


def has_legal_move(cell1, pos):
    for m in range(8):
        for n in range(8):
            if lm(cell1, chessboard[m][n], pos) and not king_will_in_danger(cell1, chessboard[m][n], pos):
                return True
    return False
