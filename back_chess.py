#!/usr/bin/env python3

"""Chess game engine"""

import pygame
from math import floor

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

   def move(self, srt, end):
      if self.board[end[0]][end[1]] != "-":
         self.board[srt[0]][srt[1]], self.board[end[0]][end[1]] = "-", self.board[srt[0]][srt[1]]
      else:   
         self.board[srt[0]][srt[1]], self.board[end[0]][end[1]] = self.board[end[0]][end[1]], self.board[srt[0]][srt[1]]

      # validity check before move
      # player change after move
      if self.white:
         self.white = False
      else:
         self.white = True

   def pawn(self, start, end):
      pass

   def rook(self, start, end):
      pass

   def knight(self, start, end):
      pass

   def bishop(self, start, end):
      pass

   def king(self, start, end):
      pass

   def queen(self, start, end):
      pass

   def boardCheck(self, start, end):
      if start[0] < 8 and start[1] < 8 and end[0] < 8 and end[1] < 8:
         return self.board[start[0]][start[1]] != "-"
      

   def turnCheck(self, start, end):
      if self.white:
         if self.board[start[0]][start[1]][0] == "b":
            return False
         return not (self.board[start[0]][start[1]][0] == "w" and self.board[end[0]][end[1]][0] == "w")
      else:
         if self.board[start[0]][start[1]][0] == "w":
            return False
         return not (self.board[start[0]][start[1]][0] == "b" and self.board[end[0]][end[1]][0] == "b")

   def ruleCheck(self, start, end):
      if self.board[start[0]][start[1]][-1] == "P":
         return self.pawn(start, end)
      elif self.board[start[0]][start[1]][-1] == "R":
         return self.rook(start, end)
      elif self.board[start[0]][start[1]][-1] == "N":
         return self.knight(start, end)
      elif self.board[start[0]][start[1]][-1] == "B":
         return self.bishop(start, end)
      elif self.board[start[0]][start[1]][-1] == "K":
         return self.king(start, end)
      elif self.board[start[0]][start[1]][-1] == "Q":
         return self.queen(start, end)

   def verify(self, start, end):
      if self.boardCheck(start, end):
         return self.turnCheck(start, end)
      return False

   @staticmethod
   def getIndex(inp):
      (y, x) = floor(inp[1] / 75), floor(inp[0] / 75)
      return (y, x)

def main():
   print("Chess backend tests")

   game = Game()

   for x in game.board:
      print(x)

   start = (6, 0)
   end = (5, 0)
   print(game.verify(start, end))
   print("------------------------")
   game.ruleCheck(start, end)
   
if __name__ == "__main__":
   main()
