#!/usr/bin/env python3

"""
Chess game using PyGame module. Main game program for chess game. Intended for 2
person multiplayer. Does not include AI for singleplayer. For details, refer to 
the README.md file.


Gameplay:
- Mouseclick based GUI. Click respective pieces to move.
- Undo button: z
- Restart button: r


Last updated: 10.Jun.2020, Python 3.8.1
By Joseph Libasora
"""

import back_chess as ch
import pygame
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

def drawGame(screen, imgs, game, validMV, clickSel):
   pygame.draw.line(screen, pygame.Color("black"), (0, 600), (600, 600), 4)
   drawBoard(screen)
   selHighlight(screen, game, validMV, clickSel)
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

def selHighlight(screen, game, validMV, clickSel):
   if clickSel != ():
      r, c = clickSel
      if game.board[r][c][0] == ("w" if game.white else "b"):
         surf = pygame.Surface((75, 75))
         surf.set_alpha(100)
         surf.fill((77, 255, 77))
         screen.blit(surf, (c * 75, r * 75))# highlight sq sel.

         for move in validMV:
            if move.start[0] == r and move.start[1] == c:
               if game.board[move.end[0]][move.end[1]][0] !=  "-" and game.board[move.end[0]][move.end[1]][0] != ("w" if game.white else "b"):
                  surf.fill((255, 51, 51))
                  screen.blit(surf, (75 * move.end[1], 75 * move.end[0]))# highlight avail. moves (n. attack)
               elif move.p_captured[-1] == "P":
                  surf.fill((255, 51, 51))
                  screen.blit(surf, (75 * move.end[1], 75 * move.end[0]))# highlight avail. moves (enP. attack)
               else:
                  surf.fill((255, 255, 153))
                  screen.blit(surf, (75 * move.end[1], 75 * move.end[0]))# highlight avail. moves (normal)

def showTime(screen, font, colour, timein, act, x, y):
   col = [(38, 38, 38), (26, 255, 26)]
   hdr = font.render(f"{colour} time:", True, col[0])
   time = font.render(timein, True, col[act])
   screen.blit(hdr, (x, y))
   screen.blit(time, (x + 15, y + 25))

def showSel(screen, font, clickSel):
   text = font.render(f"Selected {clickSel}", True, (38, 38, 38))
   screen.blit(text, (250, 615))

def showStatus(screen, font, status):
   tmp = {
      "Invalid move": 245, "": 0, "Max undo": 245, "Disabled rule check": 220,
      "Current turn: White": 205, "Current turn: Black": 205
   }
   try:
      x = tmp[status]
   except KeyError:
      x = 250
   text = font.render(status, True, (38, 38, 38))
   screen.blit(text, (x, 640))

def showPromo(screen, imgs, game):
   if game.white:
      screen.blit(imgs["w_Q"], (156, 681))
      screen.blit(imgs["w_R"], (231, 681))
      screen.blit(imgs["w_N"], (306, 681))
      screen.blit(imgs["w_B"], (381, 681))
   else:
      screen.blit(imgs["b_Q"], (156, 681))
      screen.blit(imgs["b_R"], (231, 681))
      screen.blit(imgs["b_N"], (306, 681))
      screen.blit(imgs["b_B"], (381, 681))

def main():
   print("Chess Game running")
   # other stuff here
      
   # Game init & game var. init
   pygame.init()
   game = ch.Game()
   imgs = LoadImg()
   validMV = game.getValid()
   mvMade = promo = False
   clickSel, clickLog, status = (), [], ""

   # Game screen init
   screen = pygame.display.set_mode((600, 750))
   pygame.display.set_caption("Chess")
   icon = pygame.image.load("assets/chess_icon.png")
   pygame.display.set_icon(icon)
   font = pygame.font.Font("freesansbold.ttf", 22)

   # Game time init
   w_time, b_time = ch.Time(), ch.Time()
   w_act, b_act = 1, 0
   prev_t = 0

   # Game starter drawing funct. calls
   drawGame(screen, imgs, game, validMV, clickSel)
   
   running = True
   while running:
      pygame.time.delay(100)

      # Game timer
      if not game.cm:
         if game.white:
            w_act, b_act = 1, 0
            ticks = pygame.time.get_ticks() // 1000
            if prev_t != ticks:
               w_time.add(1)
               prev_t = ticks
         else:
            w_act, b_act = 0, 1
            ticks = pygame.time.get_ticks() // 1000
            if prev_t != ticks:
               b_time.add(1)
               prev_t = ticks

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            running = False

         if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if not promo:
               pos = game.getIndex(pos)
               if pos == clickSel or pos is None:
                  clickSel, clickLog = (), []
               else:
                  clickSel = pos
                  clickLog.append(pos)
            else:
               pos = game.choiceIndex(pos)
            
            # Separate branch to deal w/ promotion
            if not promo:
               if len(clickLog) == 2:
                  mv = ch.Move(clickLog, game.board)
                  if game.turnCheck(clickLog):
                     i, mvRun = 0, True
                     while i < len(validMV) and mvRun:
                        if mv == validMV[i]:
                           print(mv)
                           mvRun = False
                           if mv.promo:
                              clickSel, clickLog, promo, status = (), [], True, "Promotion"
                           else:
                              game.mkMove(validMV[i])
                              clickSel, clickLog, status, mvMade = (), [], "", True
                        i += 1
                     if not mvMade and not promo:
                        if game.clickCheck(clickLog):
                           clickLog = [clickSel]
                        else:
                           clickSel, clickLog = (), []
                           status = "Invalid move"
                  else:
                     clickSel, clickLog = (), []
                     if game.white:
                        status = "Current turn: White"
                     else:
                        status = "Current turn: Black"
            else:
               i, mvRun = 0, True
               while i < len(validMV) and mvRun:
                  if mv == validMV[i]:
                     validMV[i].pChoice = game.gtChoice(pos)
                     game.mkMove(validMV[i])
                     promo, status, mvMade, mvRun = False, "", True, False
                  i += 1
         elif event.type == pygame.KEYDOWN:
            # Undo key, z
            if event.key == pygame.K_z:
               status = game.undo()
               mvMade = True
               if promo:
                  promo = False

      # Move made, refresh new valid moves
      if mvMade:
         validMV = game.getValid()
         mvMade = False


      # Game time fct. calls
      w_time_str, b_time_str = w_time.getTime(), b_time.getTime()
      showTime(screen, font, "White", w_time_str, w_act, 60, 615)
      showTime(screen, font, "Black", b_time_str, b_act, 435, 615)
      
      # Current selected fct. call
      showSel(screen, font, clickSel)

      # Game status fct. call
      showStatus(screen, font, status)

      # Promotion msg. fct. call
      if promo:
         showPromo(screen, imgs, game)
      
      # Main game drawing fct. call
      drawGame(screen, imgs, game, validMV, clickSel)
      pygame.display.update()
      screen.fill((179, 179, 179))

   pygame.quit()
   print(" ------ Chess game exit ------ ")
   t_time = w_time + b_time
   print(f"Total game time: {t_time}")   

if __name__ == "__main__":
   main()
