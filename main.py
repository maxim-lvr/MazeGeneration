import random
import pygame
import json
from time import sleep
import os
pygame.init()

WHITE = (255,255,255)
GREY = (20,20,20)
BLACK = (0,0,0)
PURPLE = (100,0,100)
RED = (255,0,0)

file_location = "maze_to_minecraftchunk.json"

sizex = 400
sizey = 400
size = (sizex,sizey)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Maze Generator")

done = False

clock = pygame.time.Clock()

width = 4
cols = int(size[0] / width)
rows = int(size[1] / width)

stack = []


class Cell():
    def __init__(self,x,y):
        global width
        self.x = x * width
        self.y = y * width
        
        self.visited = False
        self.current = False
        
        self.walls = [True,True,True,True] # top , right , bottom , left
        
        # neighbors
        self.neighbors = []
        
        self.top = 0
        self.right = 0
        self.bottom = 0
        self.left = 0
        
        self.next_cell = 0
    
    def draw(self):
        if self.current:
            pygame.draw.rect(screen,RED,(self.x,self.y,width,width))
        elif self.visited:
            pygame.draw.rect(screen,WHITE,(self.x,self.y,width,width))
        
            if self.walls[0]:
                pygame.draw.line(screen,BLACK,(self.x,self.y),((self.x + width),self.y),1) # top
            if self.walls[1]:
                pygame.draw.line(screen,BLACK,((self.x + width),self.y),((self.x + width),(self.y + width)),1) # right
            if self.walls[2]:
                pygame.draw.line(screen,BLACK,((self.x + width),(self.y + width)),(self.x,(self.y + width)),1) # bottom
            if self.walls[3]:
                pygame.draw.line(screen,BLACK,(self.x,(self.y + width)),(self.x,self.y),1) # left
    
    def checkNeighbors(self):
        if int(self.y / width) - 1 >= 0:
            self.top = grid[int(self.y / width) - 1][int(self.x / width)]
        if int(self.x / width) + 1 <= cols - 1:
            self.right = grid[int(self.y / width)][int(self.x / width) + 1]
        if int(self.y / width) + 1 <= rows - 1:
            self.bottom = grid[int(self.y / width) + 1][int(self.x / width)]
        if int(self.x / width) - 1 >= 0:
            self.left = grid[int(self.y / width)][int(self.x / width) - 1]
        #print("--------------------")
        
        if self.top != 0:
            if self.top.visited == False:
                self.neighbors.append(self.top)
        if self.right != 0:
            if self.right.visited == False:
                self.neighbors.append(self.right)
        if self.bottom != 0:
            if self.bottom.visited == False:
                self.neighbors.append(self.bottom)
        if self.left != 0:
            if self.left.visited == False:
                self.neighbors.append(self.left)
        
        if len(self.neighbors) > 0:
            self.next_cell = self.neighbors[random.randrange(0,len(self.neighbors))]
            return self.next_cell
        else:
            return False

def removeWalls(current_cell,next_cell):
    x = int(current_cell.x / width) - int(next_cell.x / width)
    y = int(current_cell.y / width) - int(next_cell.y / width)
    if x == -1: # right of current
        current_cell.walls[1] = False
        next_cell.walls[3] = False
    elif x == 1: # left of current
        current_cell.walls[3] = False
        next_cell.walls[1] = False
    elif y == -1: # bottom of current
        current_cell.walls[2] = False
        next_cell.walls[0] = False
    elif y == 1: # top of current
        current_cell.walls[0] = False
        next_cell.walls[2] = False

grid = []

for y in range(rows):
    grid.append([])
    for x in range(cols):
        grid[y].append(Cell(x,y))

current_cell = grid[0][0]
next_cell = 0

# -------- Main Program Loop -----------
while True:
    # --- Main event loop
    
    screen.fill(GREY)
    current_cell.visited = True
    current_cell.current = True
    
    for y in range(rows):
        for x in range(cols):
            grid[y][x].draw()
            
    
    next_cell = current_cell.checkNeighbors()
    
    if next_cell != False:
        current_cell.neighbors = []
        stack.append(current_cell)
        removeWalls(current_cell,next_cell)
        current_cell.current = False
        current_cell = next_cell
    
    elif len(stack) > 0:
        current_cell.current = False
        current_cell = stack.pop()
        
    elif len(stack) == 0:
        i = 0
        new_results = []
        for y in range(int(sizey/width)):
            for x in range(int(sizex/width)):
                pygame.image.save(screen, "screenshot.jpg")
                i += 1
                # print(y, x)
                #print(grid[y][x].walls)

                #One way
                if grid[y][x].walls == [True, True, False, True]:
                    json_data = {
                        "case": i,
                        "chunk": f"{int(x-(sizex/width)/2),int(y-(sizey/width)/2)}",
                        "structure":"blamemod:whiteroom_one",
                        "direction": 0
                        }
                    # print("one top")
                elif grid[y][x].walls == [True, True, True, False]:
                    json_data = {
                        "case": i,
                        "chunk": f"{int(x-(sizex/width)/2),int(y-(sizey/width)/2)}",
                        "structure":"blamemod:whiteroom_one",
                        "direction": 1
                        }
                    # print("one right")
                elif grid[y][x].walls == [False, True, True, True]:
                    json_data = {
                        "case": i,
                        "chunk": f"{int(x-(sizex/width)/2),int(y-(sizey/width)/2)}",
                        "structure":"blamemod:whiteroom_one",
                        "direction": 2
                        }
                    # print("one bottom")
                elif grid[y][x].walls == [True, False, True, True]:
                    json_data = {
                        "case": i,
                        "chunk": f"{int(x-(sizex/width)/2),int(y-(sizey/width)/2)}",
                        "structure":"blamemod:whiteroom_one",
                        "direction": 3
                        }
                    # print("one left")

                #two ways angle
                elif grid[y][x].walls == [True, True, False, False]:
                    json_data = {
                        "case": i,
                        "chunk": f"{int(x-(sizex/width)/2),int(y-(sizey/width)/2)}",
                        "structure":"blamemod:whiteroom_double",
                        "direction": 0
                        }
                    # print("bottom-left")
                elif grid[y][x].walls == [False, True, True, False]:
                    json_data = {
                        "case": i,
                        "chunk": f"{int(x-(sizex/width)/2),int(y-(sizey/width)/2)}",
                        "structure":"blamemod:whiteroom_double",
                        "direction": 1
                        }
                    # print("right-bottom")
                elif grid[y][x].walls == [False, False, True, True]:
                    json_data = {
                        "case": i,
                        "chunk": f"{int(x-(sizex/width)/2),int(y-(sizey/width)/2)}",
                        "structure":"blamemod:whiteroom_double",
                        "direction": 2
                        }
                    # print("top-left")
                elif grid[y][x].walls == [True, False, False, True]:
                    json_data = {
                        "case": i,
                        "chunk": f"{int(x-(sizex/width)/2),int(y-(sizey/width)/2)}",
                        "structure":"blamemod:whiteroom_double",
                        "direction": 3
                        }
                    # print("top-right")

                #two ways corridor
                elif grid[y][x].walls == [True, False, True, False]:
                    json_data = {
                        "case": i,
                        "chunk": f"{int(x-(sizex/width)/2),int(y-(sizey/width)/2)}",
                        "structure":"blamemod:whiteroom_corridor",
                        "direction": 1
                        }
                    # print("right-left")
                elif grid[y][x].walls == [False, True, False, True]:
                    json_data = {
                        "case": i,
                        "chunk": f"{int(x-(sizex/width)/2),int(y-(sizey/width)/2)}",
                        "structure":"blamemod:whiteroom_corridor",
                        "direction":0
                        }
                    # print("top-bottom")
                
                #three ways
                elif grid[y][x].walls == [True, False, False, False]:
                    json_data = {
                        "case": i,
                        "chunk": f"{int(x-(sizex/width)/2),int(y-(sizey/width)/2)}",
                        "structure":"blamemod:whiteroom_triple",
                        "direction": 0
                        }
                    # print("three no top")
                elif grid[y][x].walls == [False, True, False, False]:
                    json_data = {
                        "case": i,
                        "chunk": f"{int(x-(sizex/width)/2),int(y-(sizey/width)/2)}",
                        "structure":"blamemod:whiteroom_triple",
                        "direction": 1
                        }
                    # print("three right")
                elif grid[y][x].walls == [False, False, True, False]:
                    json_data = {
                        "case": i,
                        "chunk": f"{int(x-(sizex/width)/2),int(y-(sizey/width)/2)}",
                        "structure":"blamemod:whiteroom_triple",
                        "direction": 2
                        }
                    # print("three no bottom")
                elif grid[y][x].walls == [False, False, False, True]:
                    json_data = {
                        "case": i,
                        "chunk": f"{int(x-(sizex/width)/2),int(y-(sizey/width)/2)}",
                        "structure":"blamemod:whiteroom_triple",
                        "direction": 3
                        }
                    # print("three no left")

                #Four wayr
                elif grid[y][x].walls == [False, False, False, False]:
                    json_data = {
                        "case": i,
                        "chunk": f"{int(x-(sizex/width)/2),int(y-(sizey/width)/2)}",
                        "structure":"blamemod:whiteroom_quad",
                        "direction": 0
                        }
                    # print("four ways")
                else:
                    print("hummmmm... not supposed to happen")
                    
                new_results.append(json_data)

            if os.path.exists(file_location) and os.path.getsize(file_location) > 0:
                with open(file_location, "r+", encoding="utf-8") as file:
                    file.seek(0, os.SEEK_END)
                    pos = file.tell() - 1
                    file.seek(pos)

                    if pos > 1:
                        file.write(",")

                    json_string = json.dumps(new_results, indent=2)
                    file.write(json_string[1:])
            else:
                with open(file_location, "w", encoding="utf-8") as file:
                    json.dump(new_results, file, ensure_ascii=False, indent=2)
            new_results = []

        pygame.quit()
    
    pygame.display.flip()
    
    clock.tick(0)

