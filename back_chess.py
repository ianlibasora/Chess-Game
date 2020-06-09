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
      self.w_K, self.b_K = (7, 4), (0, 4)
      self.cm, self.stale = False, False
      

   def mkMove(self, other):
      self.board[other.start[0]][other.start[1]], self.board[other.end[0]][other.end[1]] = "-", other.p_moved
      self.moves.append(other)
      self.white = not self.white
      if other.p_moved == "w_K":
         self.w_K = (other.end[0], other.end[1])
      elif other.p_moved == "b_K":
         self.b_K = (other.end[0], other.end[1])

      if other.promo:
         self.board[other.end[0]][other.end[1]] = f"{other.p_moved[0]}_{other.pChoice}"

   def turnCheck(self, other):
      if self.white:
         return self.board[other[0][0]][other[0][1]][0] == "w"
      else:
         return self.board[other[0][0]][other[0][1]][0] == "b"

   def clickCheck(self, lst):
      l, r = self.board[lst[0][0]][lst[0][1]][0], self.board[lst[1][0]][lst[1][1]][0]
      return l == r
   
   def inCheck(self):
      if self.white:
         return self.sqAttack(self.w_K[0], self.w_K[1])
      else:
         return self.sqAttack(self.b_K[0], self.b_K[1])

   def gtChoice(self, other):
      tmp = {2: "Q", 3: "R", 4: "N", 5: "B"}
      return tmp[other[1]]

   def sqAttack(self, r, c):
      self.white = not self.white
      oMoves = self.getAllPossible()
      self.white = not self.white
      for move in oMoves:
         if move.end[0] == r and move.end[1] == c:
            return True
      return False

   def getValid(self):
      moves = self.getAllPossible()
      for i in range(len(moves) -1, -1, -1):
         self.mkMove(moves[i])
         self.white = not self.white
         if self.inCheck():
            moves.pop(i)
         self.white = not self.white
         self.undo()
      if len(moves) == 0:
         if self.inCheck():
            self.cm = True
         else:
            self.stale = True
      else:
         self.cm, self.stale = False, False
      return moves

   def getAllPossible(self):
      p_moves = []
      for r in range(8):
         for c in range(8):
            plyr, piece = self.board[r][c][0], self.board[r][c][-1]
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
      i = 1
      nrun = srun = erun = wrun = True
      if self.white:
         while nrun or srun or erun or wrun:
            if r - i < 0:
               nrun = False
            if nrun:
               if self.board[r - i][c] == "-":
                  p_moves.append(Move(((r, c), (r - i, c)), self.board))
               elif self.board[r - i][c][0] == "b":
                  p_moves.append(Move(((r, c), (r - i, c)), self.board))
                  nrun = False
               else:
                  nrun = False
            
            if 7 < r + i:
               srun = False
            if srun:
               if self.board[r + i][c] == "-":
                  p_moves.append(Move(((r, c), (r + i, c)), self.board))
               elif self.board[r + i][c][0] == "b":
                  p_moves.append(Move(((r, c), (r + i, c)), self.board))
                  srun = False
               else:
                  srun = False
            
            if c - i < 0:
               wrun = False
            if wrun:
               if self.board[r][c - i] == "-":
                  p_moves.append(Move(((r, c), (r, c - i)), self.board))
               elif self.board[r][c - i][0] == "b":
                  p_moves.append(Move(((r, c), (r, c - i)), self.board))
                  wrun = False
               else:
                  wrun = False
            
            if 7 < c + i:
               erun = False
            if erun:
               if self.board[r][c + i] == "-":
                  p_moves.append(Move(((r, c), (r, c + i)), self.board))
               elif self.board[r][c + i][0] == "b":
                  p_moves.append(Move(((r, c), (r, c + i)), self.board))
                  erun = False
               else:
                  erun = False
            i += 1
      else:
         while nrun or srun or erun or wrun:
            if 7 < r + i:
               srun = False
            if srun:
               if self.board[r + i][c] == "-":
                  p_moves.append(Move(((r, c), (r + i, c)), self.board))
               elif self.board[r + i][c][0] == "w":
                  p_moves.append(Move(((r, c), (r + i, c)), self.board))
                  srun = False
               else:
                  srun = False
         
            if r - i < 0:
               nrun = False
            if nrun:
               if self.board[r - i][c] == "-":
                  p_moves.append(Move(((r, c), (r - i, c)), self.board))
               elif self.board[r - i][c][0] == "w":
                  p_moves.append(Move(((r, c), (r - i, c)), self.board))
                  nrun = False
               else:
                  nrun = False

            if 7 < c + i:
               erun = False
            if erun:
               if self.board[r][c + i] == "-":
                  p_moves.append(Move(((r, c), (r, c + i)), self.board))
               elif self.board[r][c + i][0] == "w":
                  p_moves.append(Move(((r, c), (r, c + i)), self.board))
                  erun = False
               else:
                  erun = False

            if c - i < 0:
               wrun = False
            if wrun:
               if self.board[r][c - i] == "-":
                  p_moves.append(Move(((r, c), (r, c - i)), self.board))
               elif self.board[r][c - i][0] == "w":
                  p_moves.append(Move(((r, c), (r, c - i)), self.board))
                  wrun = False
               else:
                  wrun = False
            i += 1

   def knight(self, r, c, p_moves):
      tmp = [(-2, 1), (-2, -1), (2, 1), (2, -1), (-1, 2), (1, 2), (-1, -2), (1, -2)]
      if self.white:
         for t in tmp:
            if 0 <= r + t[0] < 8 and 0 <= c + t[1] < 8:
               if self.board[r + t[0]][c + t[1]][0] != "w":
                  p_moves.append(Move(((r, c), (r + t[0], c + t[1])), self.board))
      else:
         for t in tmp:
            if 0 <= r + t[0] < 8 and 0 <= c + t[1] < 8:
               if self.board[r + t[0]][c + t[1]][0] != "b":
                  p_moves.append(Move(((r, c), (r + t[0], c + t[1])), self.board))

   def bishop(self, r, c, p_moves):
      i = 1
      uL = uR = lL = lR = True
      if self.white:
         while uL or uR or lL or lR:
            if r - i < 0 or c - i < 0:
               uL = False
            if uL:
               if self.board[r - i][c - i] == "-":
                  p_moves.append(Move(((r, c), (r - i, c - i)), self.board))
               elif self.board[r - i][c - i][0] == "b":
                  p_moves.append(Move(((r, c), (r - i, c - i)), self.board))
                  uL = False
               else:
                  uL = False

            if r - i < 0 or 7 < c + i:
               uR = False
            if uR:
               if self.board[r - i][c + i] == "-":
                  p_moves.append(Move(((r, c), (r - i, c + i)), self.board))
               elif self.board[r - i][c + i][0] == "b":
                  p_moves.append(Move(((r, c), (r - i, c + i)), self.board))
                  uR = False
               else:
                  uR = False

            if 7 < r + i or c - i < 0:
               lL = False
            if lL:
               if self.board[r + i][c - i] == "-":
                  p_moves.append(Move(((r, c), (r + i, c - i)), self.board))
               elif self.board[r + i][c - i][0] == "b":
                  p_moves.append(Move(((r, c), (r + i, c - i)), self.board))
                  lL = False
               else:
                  lL = False

            if 7 < r + i or 7 < c + i:
               lR = False
            if lR:
               if self.board[r + i][c + i] == "-":
                  p_moves.append(Move(((r, c), (r + i, c + i)), self.board))
               elif self.board[r + i][c + i][0] == "b":
                  p_moves.append(Move(((r, c), (r + i, c + i)), self.board))
                  lR = False
               else:
                  lR = False
            i += 1
      else:
         while uL or uR or lL or lR:
            if 7 < r + i or 7 < c + i:
               lR = False
            if lR:
               if self.board[r + i][c + i] == "-":
                  p_moves.append(Move(((r, c), (r + i, c + i)), self.board))
               elif self.board[r + i][c + i][0] == "w":
                  p_moves.append(Move(((r, c), (r + i, c + i)), self.board))
                  lR = False
               else:
                  lR = False

            if 7 < r + i or c - i < 0:
               lL = False
            if lL:
               if self.board[r + i][c - i] == "-":
                  p_moves.append(Move(((r, c), (r + i, c - i)), self.board))
               elif self.board[r + i][c - i][0] == "w":
                  p_moves.append(Move(((r, c), (r + i, c - i)), self.board))
                  lL = False
               else:
                  lL = False

            if r - i < 0 or 7 < c + i:
               uR = False
            if uR:
               if self.board[r - i][c + i] == "-":
                  p_moves.append(Move(((r, c), (r - i, c + i)), self.board))
               elif self.board[r - i][c + i][0] == "w":
                  p_moves.append(Move(((r, c), (r - i, c + i)), self.board))
                  uR = False
               else:
                  uR = False

            if r - i < 0 or c - i < 0:
               uL = False
            if uL:
               if self.board[r - i][c - i] == "-":
                  p_moves.append(Move(((r, c), (r - i, c - i)), self.board))
               elif self.board[r - i][c - i][0] == "w":
                  p_moves.append(Move(((r, c), (r - i, c - i)), self.board))
                  uL = False
               else:
                  uL = False
            i += 1

   def king(self, r, c, p_moves):
      tmp = [
         (-1, -1), (-1, 0), (-1, 1), (0, -1),
         (0, 1), (1, -1), (1, 0), (1, 1)
      ]
      if self.white:
         for t in tmp:
            if 0 <= r + t[0] < 8 and 0 <= c + t[1] < 8:
               if self.board[r + t[0]][c + t[1]][0] != "w":
                  p_moves.append(Move(((r, c), (r + t[0], c + t[1])), self.board))
      else:
         for t in tmp:
            if 0 <= r + t[0] < 8 and 0 <= c + t[1] < 8:
               if self.board[r + t[0]][c + t[1]][0] != "b":
                  p_moves.append(Move(((r, c), (r + t[0], c + t[1])), self.board))

   def queen(self, r, c, p_moves):
      self.rook(r, c, p_moves)
      self.bishop(r, c, p_moves)

   def undo(self):
      if len(self.moves) != 0:
         last = self.moves.pop()
         self.board[last.start[0]][last.start[1]], self.board[last.end[0]][last.end[1]] = last.p_moved, last.p_captured
         self.white = not self.white
         if last.p_moved == "w_K":
            self.w_K = (last.start[0], last.start[1])
         elif last.p_moved == "b_K":
            self.b_K = (last.start[0], last.start[1])
         return f"Undid {last}"
      else:
         return "Max undo"

   @staticmethod
   def getIndex(inp):
      (y, x) = inp[1] // 75, inp[0] // 75
      if y < 0 or 7 < y or x < 0 or 7 < x:
         return None
      return (y, x)

   @staticmethod
   def choiceIndex(inp):
      (y, x) = inp[1] // 75, inp[0] // 75
      if y == 9 and 1 < x < 6:
         return (y, x)
      return None

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

   def __init__(self, clickLog, board, pChoice=""):
      self.start = (clickLog[0][0], clickLog[0][1])
      self.end = (clickLog[1][0], clickLog[1][1])
      self.p_moved = board[self.start[0]][self.start[1]]
      self.p_captured = board[self.end[0]][self.end[1]]
      self.moveID = (self.start[0] * 1000) + (self.start[1] * 100) + (self.end[0] * 10) + (self.end[1])
      self.pChoice = pChoice
      self.promo = False
      if (self.p_moved == "w_P" and self.end[0] == 0) or (self.p_moved == "b_P" and self.end[0] == 7):
         self.promo = True

   def getNotation(self):
      return f"{self.getRnkFile(self.start[0], self.start[1])}, {self.getRnkFile(self.end[0], self.end[1])}"

   def getRnkFile(self, r, c):
      return self.ColToFile[c] + self.RowToRnk[r]

   def __eq__(self, other):
      if isinstance(other, Move):
         return self.moveID == other.moveID
      return False

   def __str__(self):
      return self.getNotation()

class Time(object):
   def __init__(self, h=0, m=0, s=0):
      self.h, self.m, self.s = h, m, s

   def add(self, other):
      secs = self.t2s()
      self.h, self.m, self.s = self.s2t(secs + other)

   def t2s(self):
      h, m, s = self.h, self.m, self.s
      out = (h * 3600) + (m * 60) + s
      return out

   def getTime(self):
      return "{:02d}:{:02d}:{:02d}".format(self.h, self.m, self.s)

   @staticmethod
   def s2t(s):
      m, s = divmod(s, 60)
      h, m = divmod(m, 60)
      over, h = divmod(h, 24)
      return (h, m, s)

   def __str__(self):
      return "{:02d} : {:02d} : {:02d}".format(self.h, self.m, self.s)

def main():
   print("Chess backend tests")

   game = Game()
   game.board = [
         ["-", "-", "-", "-", "-", "-", "-", "-"],
         ["-", "-", "-", "-", "-", "w_P", "-", "-"],
         ["-", "-", "-", "-", "-", "-", "-", "-"],
         ["-", "-", "-", "-", "-", "-", "-", "-"],
         ["-", "-", "-", "-", "-", "-", "-", "-"],
         ["-", "-", "-", "-", "-", "-", "-", "-"],
         ["-", "-", "-", "-", "-", "-", "-", "-"],
         ["-", "-", "-", "-", "-", "-", "-", "-"],
      ]
   for x in game.board:
      print(x)
   print("--------------------------")
   valids = game.getValid()
   for x in valids:
      print(x)
      print(x.promo, x.p_moved, x.end)

   
if __name__ == "__main__":
   main()
