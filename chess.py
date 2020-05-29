#!/usr/bin/env python3

"""Chess game"""

import back_chess as ch
import pygame

# block space = 70
# 276, 95

def LoadImg():
   imgs = {}
   pieces = [
      "b_R", "b_N", "b_B", "b_Q", "b_K", "b_P",
      "w_R", "w_N", "w_B", "w_Q", "w_K", "w_P"
      ]
   for x in pieces:
      imgs[x] = pygame.image.load(f"assets/{x}.png")
   return imgs

def drawGame(screen, backg, imgs, game):
   screen.fill((255, 255, 204))
   drawBoard(screen, backg)
   drawPieces(screen, imgs, game.board)

def drawBoard(screen, backg):
   pass
   # for r in range(8):
   #    for c in range(8):
   #       pygame.Rect(r * 67)

def drawPieces(screen, imgs, board):
   for r in range(8):
      for c in range(8):
         if board[r][c] != "-":
            screen.blit(imgs[board[r][c]], (276 + (67 * c), 95 + (67 * r)))

def main():
   print("Chess Game By Joseph Libasora running")
   # other stuff here


   pygame.init()
   game = ch.Game()
   imgs = LoadImg()


   screen = pygame.display.set_mode((1024, 700))
   pygame.display.set_caption("Chess")
   icon = pygame.image.load("assets/chess_icon.png")
   pygame.display.set_icon(icon)
   backg = pygame.image.load("assets/cboard.png")

      
   text = pygame.font.Font("freesansbold.ttf", 32) #tmp

   drawGame(screen, backg, imgs, game)

   running = True
   while running:


      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            running = False

      drawGame(screen, backg, imgs, game)

      pygame.display.update()

   pygame.quit()
   print("Game exit")

if __name__ == "__main__":
   main()
