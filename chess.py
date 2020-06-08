#!/usr/bin/env python3

"""Chess game"""

import back_chess as ch
import pygame
from sys import argv
import time


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
   pygame.draw.line(screen, pygame.Color("black"), (0, 600), (600, 600), 4)
   drawBoard(screen)
   drawPieces(screen, imgs, game.board)


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


def showTime(screen, font, colour, time, x, y):
   text = font.render(f"{colour} time: {time}", True, (38, 38, 38))
   screen.blit(text, (x, y))

def showSel(screen, font, clickSel):
   text = font.render(f"Selected {clickSel}", True, (38, 38, 38))
   screen.blit(text, (250, 615))

def showStatus(screen, font, status):
   text = font.render(f"Status: {status}", True, (38, 38, 38))
   screen.blit(text, (180, 650))

def main():
   print("Chess Game running")
   # other stuff here

   args = argv[1:]
   if len(args) != 0:
      if args[0] == "1":
         ruleOveride = True
         status = "Disabled rule check"
      else:
         ruleOveride = False
         status = "Noninal"
   else:
      ruleOveride = False
      status = "Nominal"

   pygame.init()
   game = ch.Game()
   imgs = LoadImg()
   validMV = game.getValid()
   mvMade = False

   screen = pygame.display.set_mode((600, 720))
   pygame.display.set_caption("Chess")
   icon = pygame.image.load("assets/chess_icon.png")
   pygame.display.set_icon(icon)
   font = pygame.font.Font("freesansbold.ttf", 16)


   w_time, b_time = ch.Time(), ch.Time()
   prev_t = 0

   drawGame(screen, imgs, game)
   clickSel, clickLog = (), []
   running = True
   while running:
      if game.white:
         ticks = pygame.time.get_ticks() // 1000
         if prev_t != ticks:
            w_time.add(1)
            prev_t = ticks
      else:
         ticks = pygame.time.get_ticks() // 1000
         if prev_t != ticks:
            b_time.add(1)
            prev_t = ticks

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            running = False

         if pygame.mouse.get_pressed() and event.type == pygame.MOUSEBUTTONDOWN:
            pos = game.getIndex(pygame.mouse.get_pos())
            if pos == clickSel or pos is None:
               clickSel, clickLog = (), []
            else:
               clickSel = pos
               clickLog.append(pos)
            
            if len(clickLog) == 2:
               mv = ch.Move(clickLog, game.board)
               if game.turnCheck(clickLog):
                  if ruleOveride or mv in validMV:
                     game.mkMove(mv)
                     print(mv)
                     mvMade = True
                     clickSel, clickLog = (), []
                     status = ""
                  else:
                     if game.clickCheck(clickLog):
                        clickLog = [clickSel]
                     else:
                        clickSel, clickLog = (), []
                        if game.white:
                           status = "Invalid move, white turn"
                        else:
                           status = "Invalid move, black turn"
               else:
                  clickSel, clickLog = (), []
                  if game.white:
                     status = "Current turn: White"
                  else:
                     status = "Current turn: Black"
         elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
               game.undo()
               mvMade = True

      if mvMade:
         validMV = game.getValid()
         mvMade = False


      w_time_str, b_time_str = w_time.getTime(), b_time.getTime()
      showTime(screen, font, "White", w_time_str, 20, 615)
      showTime(screen, font, "Black", b_time_str, 400, 615)
      showSel(screen, font, clickSel)
      showStatus(screen, font, status)
      drawGame(screen, imgs, game)
      

      pygame.display.update()
      screen.fill((191, 191, 191))

   pygame.quit()
   print("Game exit")
   

if __name__ == "__main__":
   main()
