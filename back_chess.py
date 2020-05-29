#!/usr/bin/env python3

"""Chess game objects"""

class Piece(object):
   def __init__(self, team):
      self.team = team

   def __str__(self):
      return self.team

class Pawn(Piece):
   pass

class Rook(Piece):
   pass

class Horse(Piece):
   pass

class Bishop(Piece):
   pass

class King(Piece):
   pass

class Queen(Piece):
   pass

def main():
   print("chess-obj tests")

   one = Piece("Black")
   two = Piece("White")
   

if __name__ == "__main__":
   main()
