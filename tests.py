# -*- coding: utf-8 -*-
import unittest
import numpy as np
from conf import conf
from self_play import (
        color_board, _get_points, capture_group, make_play, legal_moves,
        index2coord,
)

class TestGoMethods(unittest.TestCase):
    def assertEqualList(self, arr1, arr2):
        self.assertEqual(arr1.tolist(), arr2.tolist())

    def test_coloring_player_1(self):
        board = np.array(
                         [[1, 1, 1],
                          [1, 0, 1],
                          [1, 1, 1]]) 
        target = np.array(
                         [[1, 1, 1],
                          [1, 1, 1],
                          [1, 1, 1]]) 
        self.assertEqualList(color_board(board, 1), target)
        board = np.array(
                         [[1, 1, 1, -1, -1, -1],
                          [1, 0, 1, -1,  0, -1],
                          [1, 1, 1, -1, -1, -1]]) 
        target = np.array(
                         [[1, 1, 1, -1, -1, -1],
                          [1, 1, 1, -1,  0, -1],
                          [1, 1, 1, -1, -1, -1]]) 
        self.assertEqualList(color_board(board, 1), target)

    def test_player_1_big(self):
        board = np.array([
                 [0,  0,  0,  1,  0, -1,  0,  0,  0,], 
                 [0,  0,  0,  1,  0, -1,  0,  0,  0,],
                 [0,  0,  0,  1,  0, -1,  0,  0,  0,],
                 [0,  0,  0,  1, -1,  0,  0, -1,  0,],
                 [1,  1,  1, -1,  0, -1, -1,  0,  0,],
                 [0,  0,  0,  1, -1,  0,  0, -1, -1,],
                 [0,  0,  0,  1,  0, -1,  0,  0,  0,],
                 [0,  0,  0,  1,  0, -1,  0,  1,  0,],
                 [0,  0,  0,  0,  0, -1,  0,  0,  0,],
        ])
        target = np.array([
                 [1,  1,  1,  2,  0, -2, -1, -1, -1,], 
                 [1,  1,  1,  2,  0, -2, -1, -1, -1,],
                 [1,  1,  1,  2,  0, -2, -1, -1, -1,],
                 [1,  1,  1,  2, -2, -1, -1, -2, -1,],
                 [2,  2,  2, -2, -1, -2, -2, -1, -1,],
                 [0,  0,  0,  2, -2,  0,  0, -2, -2,],
                 [0,  0,  0,  2,  0, -2,  0,  0,  0,],
                 [0,  0,  0,  2,  0, -2,  0,  2,  0,],
                 [0,  0,  0,  0,  0, -2,  0,  0,  0,],
        ]) 
        colored1 = color_board(board,  1)
        colored2 = color_board(board, -1)
        total = colored1 + colored2
        self.assertEqualList(total, target)

    def test_coloring_player_2(self):
        board = np.array(
                         [[1, 1, 1],
                          [1, 0, 1],
                          [1, 1, 1]]) 
        target = np.array(
                         [[1, 1, 1],
                          [1, 0, 1],
                          [1, 1, 1]]) 
        self.assertEqualList(color_board(board, -1), target)
        board = np.array(
                         [[1, 1, 1, -1, -1, -1],
                          [1, 0, 1, -1,  0, -1],
                          [1, 1, 1, -1, -1, -1]]) 
        target = np.array(
                         [[1, 1, 1, -1, -1, -1],
                          [1, 0, 1, -1, -1, -1],
                          [1, 1, 1, -1, -1, -1]]) 
        self.assertEqualList(color_board(board, -1), target)

    def test_get_winner(self):
        board = np.array([
                 [0,  0,  0,  1,  0, -1,  0,  0,  0,], 
                 [0,  0,  0,  1,  0, -1,  0,  0,  0,],
                 [0,  0,  0,  1,  0, -1,  0,  0,  0,],
                 [0,  0,  0,  1, -1,  0,  0, -1,  0,],
                 [1,  1,  1, -1,  0, -1, -1,  0,  0,],
                 [0,  0,  0,  1, -1,  0,  0, -1, -1,],
                 [0,  0,  0,  1,  0, -1,  0,  0,  0,],
                 [0,  0,  0,  1,  0, -1,  0,  1,  0,],
                 [0,  0,  0,  0,  0, -1,  0,  0,  0,],
        ])
        self.assertEqual(_get_points(board), {0: 29, 1: 12, 2: 11, -1: 15, -2: 14})

    def test_taking_stones(self):
        board = np.array(
                         [[0, 1, 0],
                          [1,-1, 1],
                          [0, 1, 0]]) 
        target_group = [(1, 1)]
        group = capture_group(1, 1, board)
        self.assertEqual(group, target_group)

    def test_taking_group_stones(self):
        board = np.array(
                         [[0, 1, 0],
                          [1,-1, 1],
                          [1,-1, 1],
                          [0, 1, 0]]) 
        target_group = [(1, 1), (1, 2)]
        group = capture_group(1, 1, board)
        self.assertEqual(group, target_group)

        target_group = [(1, 2), (1, 1)]
        group = capture_group(1, 2, board)
        self.assertEqual(group, target_group)

    def test_taking_group_stones_sides(self):
        board = np.array(
                         [[-1, 1, 0],
                          [ 1, 0, 0],
                          [ 0, 0, 0]])
        target_group = [(0, 0)]
        group = capture_group(0, 0, board)
        self.assertEqual(group, target_group)

        board = np.array(
                         [[-1,-1, 1],
                          [ 1, 1, 0],
                          [ 0, 0, 0]])
        target_group = [(0, 0), (1, 0)]
        group = capture_group(0, 0, board)
        self.assertEqual(group, target_group)

        target_group = [(1, 0), (0, 0)]
        group = capture_group(1, 0, board)
        self.assertEqual(group, target_group)

    def test_taking_group_sucide(self):
        board = np.array(
                         [[-1, 1, 0],
                          [ 1, 0, 0],
                          [ 0, 0, 0]])
        target_group = [(0, 0)]
        group = capture_group(0, 0, board)
        self.assertEqual(group, target_group)

        board = np.array(
                         [[-1,-1, 1],
                          [ 1, 1, 0],
                          [ 0, 0, 0]])
        target_group = [(0, 0), (1, 0)]
        group = capture_group(0, 0, board)
        self.assertEqual(group, target_group)

        target_group = [(1, 0), (0, 0)]
        group = capture_group(1, 0, board)
        self.assertEqual(group, target_group)

    def test_circle_group(self):
        board = np.array(
                         [[ 0, 1, 1, 1, 0],
                          [ 1,-1,-1,-1, 1],
                          [ 1,-1, 1,-1, 1],
                          [ 1,-1,-1,-1, 1],
                          [ 0, 1, 1, 1, 0]])
        target_group = [(1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (1, 2)]
        self.assertEqual(len(target_group), 8)
        for x, y in target_group:
            group = capture_group(x, y, board)
            self.assertEqual(sorted(group), sorted(target_group))

class TestBoardMethods(unittest.TestCase):
    def test_self_sucide(self):
        board = np.zeros((1, 19, 19, 17), dtype=np.float32)
        player = 1
        board[:,:,:,-1] = player

        make_play(0, 0, board) # black
        make_play(1, 0, board) # white
        make_play(8, 9, board) # black random
        make_play(2, 1, board) # white
        make_play(8, 8, board) # black random pos
        make_play(3, 0, board) # white
        # ○ ● . ● . .
        # . . ● . . .
        # . . . . . .
        make_play(2, 0, board) # black sucides
        self.assertEqual(board[0][0][1][0], 1) # white stone
        self.assertEqual(board[0][0][1][1], 0) # was not taken

        self.assertEqual(board[0][0][2][0], 0) # black stone
        self.assertEqual(board[0][0][2][1], 0) # was taken

    def test_legal_moves_ko(self):
        board = np.zeros((1, 19, 19, 17), dtype=np.float32)
        player = 1
        board[:,:,:,-1] = player

        make_play(0, 0, board) # black
        make_play(1, 0, board) # white
        make_play(1, 1, board) # black
        make_play(2, 1, board) # white
        make_play(8, 8, board) # black random pos
        make_play(3, 0, board) # white
        # ○ ● . ● . .
        # . ○ ● . . .
        # . . . . . .
        make_play(2, 0, board) # black captures_first
        # ○ . ○ ● . .
        # . ○ ● . . .
        # . . . . . .
        mask = legal_moves(board)
        self.assertEqual(board[0][0][1][0], 0) # white stone
        self.assertEqual(board[0][0][1][1], 0) # was taken
        self.assertEqual(board[0][0][1][2], 1) # white stone was here
        self.assertEqual(board[0][0][1][3], 0) # black stone was not here
        self.assertEqual(mask[1], True)

    def test_legal_moves_not_ko(self):
        board = np.zeros((1, 19, 19, 17), dtype=np.float32)
        player = 1
        board[:,:,:,-1] = player

        make_play(0, 0, board) # black
        make_play(1, 0, board) # white
        make_play(1, 1, board) # black
        make_play(2, 0, board) # white
        make_play(2, 1, board) # black
        make_play(8, 8, board) # white random pos
        # ○ ● ● . . .
        # . ○ ○ . . .
        # . . . . . .
        make_play(3, 0, board) # black captures_first
        # ○ . . ○ . .
        # . ○ ○ . . .
        # . . . . . .
        mask = legal_moves(board)
        self.assertEqual(board[0][0][1][0], 0) # white stone 1
        self.assertEqual(board[0][0][1][1], 0) # was taken
        self.assertEqual(board[0][0][2][0], 0) # white stone 2
        self.assertEqual(board[0][0][2][1], 0) # was taken
        self.assertEqual(board[0][0][1][2], 1) # white stone 1 was here
        self.assertEqual(board[0][0][1][3], 0) # black stone was not here
        self.assertEqual(board[0][0][2][2], 1) # white stone 2 was here
        self.assertEqual(board[0][0][2][3], 0) # black stone was not here
        self.assertEqual(mask[1], False)
        self.assertEqual(mask[2], False)

    def test_full_board_capture(self):
        size = conf['SIZE']
        board = np.zeros((1, size, size, 17), dtype=np.float32)
        player = 1
        board[:,:,:,-1] = player

        for i in range(size*size - 2):
            x, y = index2coord(i)
            make_play(x, y, board) # black
            make_play(0, size, board) # white pass

        # ○ ○ ○ ○ ○ ○
        # ○ ○ ○ ○ ○ ○
        # ○ ○ ○ ○ ○ ○
        # ○ ○ ○ ○ . .
        make_play(0, size, board) # black pass
        make_play(size -1, size - 1, board) # white corner
        # ○ ○ ○ ○ ○ ○
        # ○ ○ ○ ○ ○ ○
        # ○ ○ ○ ○ ○ ○
        # ○ ○ ○ ○ . ●

        for i in range(size*size - 2):
            x, y = index2coord(i)
            self.assertEqual(board[0][y][x][0], 1) # black stone i
            self.assertEqual(board[0][y][x][1], 0) # black stone i

        self.assertEqual(board[0][size - 1][size - 1][0], 0) # white stone
        self.assertEqual(board[0][size - 1][size - 1][1], 1) # white stone
        self.assertEqual(board[0][size - 1][size - 2][0], 0) # empty
        self.assertEqual(board[0][size - 1][size - 2][1], 0) # empty

        make_play(size - 2, size - 1, board) # black
        # ○ ○ ○ ○ ○ ○
        # ○ ○ ○ ○ ○ ○
        # ○ ○ ○ ○ ○ ○
        # ○ ○ ○ ○ ○ .
        for i in range(size*size - 1):
            x, y = index2coord(i)
            self.assertEqual(board[0][y][x][0], 0) # black stone i
            self.assertEqual(board[0][y][x][1], 1) # black stone i (it's white's turn)
        self.assertEqual(board[0][size - 1][size - 1][0], 0) # empty
        self.assertEqual(board[0][size - 1][size - 1][1], 0) # empty

        make_play(size - 1, size - 1, board) # white
        # . . . . . .
        # . . . . . .
        # . . . . . .
        # . . . . . ●
        for i in range(size*size - 1):
            x, y = index2coord(i)
            self.assertEqual(board[0][y][x][0], 0) # empty
            self.assertEqual(board[0][y][x][1], 0) # empty
        self.assertEqual(board[0][size - 1][size - 1][0], 0) # white
        self.assertEqual(board[0][size - 1][size - 1][1], 1) # white

    def test_bug(self):
        # ● ● ● ● ● ● ● ● ●
        # ● ● ● ● ● ● ● ● ●
        # ● ● ● ● ● ● ● ● ●
        # ● ● ● ● ● ● ● ● ●
        # ● ● ● ● ● ● ● ● ●
        # ● ● ● ● ● ● ● ● ●
        # ● ● ● ● ● ○ ○ ● ●
        # ● ● ● ● ● ● . ● ●
        # ● ● ● ● ● ● ○ ○ ○
        size = conf['SIZE']
        board = np.zeros((1, size, size, 17), dtype=np.float32)
        player = 1
        board[:,:,:,-1] = player

        for i in range(size*size):
            x, y = index2coord(i)
            if (x, y) in [(5, 6), (6, 6), (6, 8), (7, 8), (8, 8)]:
                make_play(x, y, board) # black
                make_play(0, size, board) # white pass
            elif (x, y) in [(6, 7)]:
                make_play(0, size, board) # black pass
                make_play(0, size, board) # white pass
            else:
                make_play(0, size, board) # black pass
                make_play(x, y, board) # white

        make_play(0, size, board) # black pass
        make_play(6, 7, board) # white

        # ● ● ● ● ● ● ● ● ●
        # ● ● ● ● ● ● ● ● ●
        # ● ● ● ● ● ● ● ● ●
        # ● ● ● ● ● ● ● ● ●
        # ● ● ● ● ● ● ● ● ●
        # ● ● ● ● ● ● ● ● ●
        # ● ● ● ● ● . . ● ●
        # ● ● ● ● ● ● ● ● ●
        # ● ● ● ● ● ● . . . 
        for i in range(size*size - 1):
            x, y = index2coord(i)
            if (x, y) in [(5, 6), (6, 6), (6, 8), (7, 8), (8, 8)]:
                self.assertEqual(board[0][y][x][0], 0) # empty
                self.assertEqual(board[0][y][x][1], 0) # emtpy
            else:
                self.assertEqual(board[0][y][x][0], 0) # white
                self.assertEqual(board[0][y][x][1], 1) # white




if __name__ == '__main__':
    unittest.main()
