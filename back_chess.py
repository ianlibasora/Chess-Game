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
      self.moves = []
      self.dct = {
         "P": self.pawn, "R": self.rook, "N": self.knight,
         "B": self.bishop, "K": self.king, "Q": self.queen
      }

   def mkMove(self, other):
      self.board[other.start[0]][other.start[1]], self.board[other.end[0]][other.end[1]] = "-", other.p_moved
      self.moves.append(other)
      self.white = not self.white

   def turnCheck(self, other):
      if self.white:
         return (self.board[other[0][0]][other[0][1]][0] == "w" and self.board[other[1][0]][other[1][1]][0] != "w")
      else:
         return (self.board[other[0][0]][other[0][1]][0] == "b" and self.board[other[1][0]][other[1][1]][0] != "b")

   def getValid(self):
      return self.getAllPossible()

   def getAllPossible(self):
      p_moves = []
      for r in range(8):
         for c in range(8):
            piece = self.board[r][c][-1]
            plyr = self.board[r][c][0]
            if (plyr == "w" and self.white) or (plyr == "b" and not self.white):
               self.dct[piece](r, c, p_moves)
      return p_moves

   def pawn(self, r, c, p_moves):
      if self.white:
         if self.board[r - 1][c] == "-":
            p_moves.append(Move(((r, c), (r - 1, c)), self.board))
            if r == 6 and self.board[r - 2][c] == "-":
               p_moves.append(Move(((r, c), (r - 2, c)), self.board))
         
         if 0 <= c - 1:
            if self.board[r - 1][c - 1][0] == "b":
               p_moves.append(Move(((r, c), (r - 1, c - 1)), self.board))
         if c + 1 < 8:
            if self.board[r - 1][c + 1][0] == "b":
               p_moves.append(Move(((r, c), (r - 1, c + 1)), self.board))
         
      else:
         if self.board[r + 1][c] == "-":
            p_moves.append(Move(((r, c), (r + 1, c)), self.board))
            if r == 1 and self.board[r + 2][c] == "-":
               p_moves.append(Move(((r, c), (r + 2, c)), self.board))
         
         if 0 <= c - 1:
            if self.board[r + 1][c - 1][0] == "w":
               p_moves.append(Move(((r, c), (r + 1, c - 1)), self.board))
         if c + 1 < 8:
            if self.board[r + 1][c + 1][0] == "w":
               p_moves.append(Move(((r, c), (r + 1, c + 1)), self.board))

   def rook(self ,r, c, p_moves):
      pass

   def knight(self, r, c, p_moves):
      pass

   def bishop(self, r, c, p_moves):
      pass

   def king(self, r, c, p_moves):
      pass

   def queen(self, r, c, p_moves):
      pass

   def undo(self):
      if len(self.moves) != 0:
         last = self.moves[-1]
         self.board[last.start[0]][last.start[1]], self.board[last.end[0]][last.end[1]] = last.p_moved, last.p_captured
         print(f"Undid {last}")
         self.moves.pop()
         self.white = not self.white
      else:
         print("Max undo")

   def nextPlyr(self):
      if self.white:
         print("Next move: White")
      else:
         print("Next move: Black")

   @staticmethod
   def getIndex(inp):
      (y, x) = inp[1] // 75, inp[0] // 75
      if y < 0 or 7 < y or x < 0 or 7 < x:
         return None
      else:
         return (y, x)

class Move(object):
   RnkToRow = {
      "1": 7, "2":6, "3": 5, "4": 4,
      "5": 3, "6": 2, "7": 1, "8": 0
   }
   RowToRnk = {v: k for k, v in RnkToRow.items()}
   FileToCol = {
      "a": 0, "b": 1, "c": 2, "d": 3,
      "e": 4, "f": 5, "g": 6, "h": 7
   }
   ColToFile = {v: k for k, v in FileToCol.items()}

   def __init__(self, clickLog, board):
      self.start = (clickLog[0][0], clickLog[0][1])
      self.end = (clickLog[1][0], clickLog[1][1])
      self.p_moved = board[self.start[0]][self.start[1]]
      self.p_captured = board[self.end[0]][self.end[1]]
      self.moveID = self.start[0] * 1000 + self.start[1] * 100 + self.end[0] * 10 + self.end[1]

   def getNotation(self):
      return f"{self.getRnkFile(self.start[0], self.start[1])} -> {self.getRnkFile(self.end[0], self.end[1])}"

   def getRnkFile(self, r, c):
      return self.ColToFile[c] + self.RowToRnk[r]

   def __eq__(self, other):
      if isinstance(other, Move):
         return self.moveID == other.moveID
      return False

   def __str__(self):
      return self.getNotation()

def main():
   print("Chess backend tests")

   game = Game()

   for x in game.board:
      print(x)
   
   clickLog = [(6, 1), (5, 1)]

   mv = Move(clickLog, game.board)
   print(mv)
   game.mkMove(mv)

   for x in game.board:
      print(x)

   print("--------------------------")
   print(game.getAllPossible())
   
if __name__ == "__main__":
   main()
