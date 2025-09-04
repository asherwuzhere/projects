#import sys
'''import pygame
import time

pygame.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Analysing Brainwaves")

def show_loading_screen():
    screen.fill((0,0,0))
    font = pygame.font.SysFont(None, 55)
    text = font.render("Loading...", True, (255, 255, 255))
    screen.blit(text, (100, 130))
    pygame.display.update()

def load_assets():
    for i in range(5):
        print(f"Loading asset {i+1}")
        time.sleep(1)

def main():
     running = True
     show_loading_screen()
     load_assets()

     while running:
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 running = False

         screen.fiull((0,0,255))
         pygame.display.update()

     pygame.quit()

if __name__ == "__main__":
    main()
'''

import time

while True:
    number = input("Think of a number and type it in: ")

    if number.lower() == "exit":
        print("Thanks for playing, goodbye!")
        break

    time.sleep(1)
    print("Analysing Brain Waves.", end="", flush=True)
    time.sleep(0.5)
    print(".", end="", flush=True)
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    print("Decoding Neural Patterns.", end="", flush=True)
    time.sleep(0.5)
    print(".", end="", flush=True)
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    print("Accessing Subconscious Frameworks.", end="", flush=True)
    time.sleep(0.5)
    print(".", end="", flush=True)
    time.sleep(0.5)
    print(".")
    time.sleep(0.5)
    print("Mapping Cognitive Pathways.", end="", flush=True)
    time.sleep(0.5)
    print(".", end="", flush=True)
    time.sleep(0.5)
    print(".")
    time.sleep(2)

    print()
    print(f"The number you were thinking of was: {number}")
    print()
