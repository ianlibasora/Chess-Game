#!/usr/bin/env python3

"""Chess game engine"""

import pygame

class Game(object):
   def __init__(self):
      self.board = [
         ["b_R", "b_N", "b_B", "b_Q", "b_K", "b_B", "b_N", "b_R"],
         ["b_P", "b_P", "b_P", "b_P", "b_P", "b_P", "b_P", "b_P"],
         ["-", "-", "-", "-", "-", "-", "-", "-"],
         ["-", "-", "-", "-", "-", "-", "-", "-"],
         ["-", "-", "-", "-", "-", "-", "-", "-"],
         ["-", "-", "-", "-", "-", "-", "-", "-"],
         ["w_P", "w_P", "w_P", "w_P", "w_P", "w_P", "w_P", "w_P"],
         ["w_R", "w_N", "w_B", "w_Q", "w_K", "w_B", "w_N", "w_R"],
      ]
      self.white = True


def main():
   print("chess engine tests")

   game = Game()
   print(board.board)

if __name__ == "__main__":
   main()
