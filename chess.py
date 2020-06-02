#!/usr/bin/env python3

"""Chess game"""

import back_chess as ch
import pygame
from sys import argv

def LoadImg():
   imgs = {}
   pieces = [
      "b_R", "b_N", "b_B", "b_Q", "b_K", "b_P",
      "w_R", "w_N", "w_B", "w_Q", "w_K", "w_P"
      ]
   for x in pieces:
      imgs[x] = pygame.image.load(f"assets/{x}.png")
   return imgs

def drawGame(screen, imgs, game):
   screen.fill((191, 191, 191))
   pygame.draw.line(screen, pygame.Color("black"), (0, 600), (600, 600), 4 )
   drawBoard(screen)
   drawPieces(screen, imgs, game.board)
   # drawTime(screen, game.white)

def drawBoard(screen):
   cols = [pygame.Color("white"), pygame.Color("grey")]
   for r in range(8):
      for c in range(8):
         col = cols[(r + c) % 2]
         pygame.draw.rect(screen, col, pygame.Rect(c * 75, r * 75, 75, 75))

def drawPieces(screen, imgs, board):
   for r in range(8):
      for c in range(8):
         if board[r][c] != "-":
            screen.blit(imgs[board[r][c]], (6 + (75 * c), 6 + (75 * r)))

def main():
   print("Chess Game running")
   # other stuff here

   try:
      args = argv[1:]
      if args[0] == "1":
         ruleOveride = True
   except IndexError:
      ruleOveride = False
      print("No args, running normally")

   pygame.init()
   game = ch.Game()
   imgs = LoadImg()
   validMV = game.getValid()
   mvMade = False

   screen = pygame.display.set_mode((600, 720))
   pygame.display.set_caption("Chess")
   icon = pygame.image.load("assets/chess_icon.png")
   pygame.display.set_icon(icon)


   drawGame(screen, imgs, game)
   clickSel = ()
   clickLog = []
   running = True
   while running:
      pygame.time.delay(50)


      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            running = False

         if pygame.mouse.get_pressed() and event.type == pygame.MOUSEBUTTONDOWN:
            pos = game.getIndex(pygame.mouse.get_pos())
            if pos == clickSel or pos is None:
               clickSel = ()
               clickLog = []
            else:
               clickSel = pos
               clickLog.append(pos)
            
            if len(clickLog) == 2:
               if game.turnCheck(clickLog):
                  mv = ch.Move(clickLog, game.board)
                  print(clickLog)

                  if ruleOveride or mv in validMV:
                     game.mkMove(mv)
                     print(mv)
                     game.nextPlyr()
                     mvMade = True
                  clickSel = ()
                  clickLog = []
               else:
                  clickSel = ()
                  clickLog = []
                  if game.white:
                     print("Invalid move, current turn: White")
                  else:
                     print("Invalid move, current turn: Black")
         elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
               game.undo()
               mvMade = True

      if mvMade:
         validMV = game.getValid()
         mvMade = False




      # validity checks
      # ch.move(start, end)
      # need sys to find mouse clicks, corresponding pos, corresponding grid ref.
      

      drawGame(screen, imgs, game)

      pygame.display.update()

   pygame.quit()
   print("Game exit")

if __name__ == "__main__":
   main()
