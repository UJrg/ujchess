#!/usr/bin/env python
# -*- coding: utf-8 -*-
from legal_moves import *


def every_legal_move(color, pos):
    pos_moves = []
    for key in pos:
        for m in range(8):
            for n in range(8):
                if pos[key][0] == color and lm(key, chessboard[m][n], pos) and not \
                        king_will_in_danger(key, chessboard[m][n], pos):
                    pos_moves.append([key, chessboard[m][n]])
    return pos_moves

def optimize_lis(lis, pos):
    spec_lis = []
    for move in lis:
        if can_checkmate(pos, 'W'):
            spec_lis.append(move)
            return spec_lis

    res = []
    for move in lis:
        if not attack_move(pos, 'B', move):
            res.append(move)
    if len(res) != 0:
        lis = res
        res = []
    else:
        return lis

    for move in lis:
        if not piece_will_in_danger(pos, 'Q', 'B', move):
            res.append(move)
    if len(res) != 0:
        lis = res
        res = []
    else:
        return lis

    for move in lis:
        if not mains_will_in_danger(pos, 'B', move):
            res.append(move)
    if len(res) != 0:
        lis = res
        res = []
    else:
        return lis

    for move in lis:
        if u_kill_something(pos, move, 'Q', 'W') or u_kill_mains(pos, move, 'W') or attack_move(pos, 'W', move):
            res.append(move)
    if len(res) != 0:
        lis = res
    else:
        return lis
    return lis


def piece_in_danger(pos, piece, color):
    for key in pos:
        if pos[key][1] == piece:
            piece_cell = key
            for keys in pos:
                if pos[keys][0] != color and lm(keys, piece_cell, pos):
                    return True
    return False


def piece_will_in_danger(pos, piece, color, move):
    var_pos = pos.copy()
    var_pos[move[1]] = var_pos[move[0]]
    del var_pos[move[0]]
    return piece_in_danger(var_pos, piece, color)


def u_kill_something(pos, move, piece, color):
    if move[1] in pos and pos[move[1]] == color + piece:
        return True
    return False


def u_kill_mains(pos, move, color):
    return u_kill_something(pos, move, 'R', color) or \
           u_kill_something(pos, move, 'B', color) or u_kill_something(pos, move, 'N', color)


def mains_in_danger(pos, color):
    if piece_in_danger(pos, 'R', color) or piece_in_danger(pos, 'B', color) or piece_in_danger(pos, 'N', color):
        return True
    return False


def mains_will_in_danger(pos, color, move):
    var_pos = pos.copy()
    var_pos[move[1]] = var_pos[move[0]]
    del var_pos[move[0]]
    return mains_in_danger(var_pos, color)


def will_checkmate(pos, color, move):
    var_pos = pos.copy()
    var_pos[move[1]] = var_pos[move[0]]
    del var_pos[move[0]]
    if color == 'W':
        color = 'B'
    else:
        color = 'W'
    if is_mate(color, var_pos):
        return True
    return False


def can_checkmate(pos, color):
    for key in pos:
        if pos[key][0] != color:
            for m in range(8):
                for n in range(8):
                    if lm(key, chessboard[m][n], pos):
                        var_pos = pos.copy()
                        var_pos[chessboard[m][n]] = var_pos[key]
                        del var_pos[key]
                        if is_mate(color, var_pos):
                            return True
    return False


def attack_move(pos, color, move):
    var_pos = pos.copy()
    var_pos[move[1]] = var_pos[move[0]]
    del var_pos[move[0]]
    return can_checkmate(var_pos, color)
