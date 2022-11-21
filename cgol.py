import random
import os
from pynput.keyboard import Key, Listener

os.system('cls')

ROWS = 100
COLS = 100

arr = [[0 for i in range(COLS)] for j in range(ROWS)]

ctr = 0

# arr = [[1,0,1,0,0],
# [1,1,0,1,1],
# [1,1,0,1,0],
# [0,1,1,1,1],
# [0,1,0,1,0]]

# ROWS = len(arr)
# COLS = len(arr[0])

def printcell(cellval):
    if (cellval == 1):
        print("■", end=" ")
    else:
        print(" ", end=" ")

def getLiveNeighbourCount(arr, x, y):
    live = 0
    for i in range(0,3):
        for j in range(0, 3):
            nrow = x-1+i
            ncol = y-1+j
            if (nrow != -1 and ncol != -1):
                try:
                    cell = arr[nrow][ncol]
                except IndexError:
                    cell = 0

                if (cell == 1):
                    live+=1
    if (arr[x][y] == 1):
        live-=1
    return live

def on_init_press(key):
    if (key == Key.enter):
        global arr
        # Reading cell values from a file
        # Reading the file and putting it into the array.
        file = open("input.txt", "r")
        file_data = file.read()
        i = 0
        for line in file_data.split():
            j = 0
            for letter in line:
                arr[i][j] = int(line[j])
                j+=1
            i+=1

        print("File loaded...")
        for i in range(ROWS):
            for j in range(COLS):
                printcell(arr[i][j])
            print("")

def on_init_release(key):
    if (key == Key.enter):
        return False

def on_press(key):
    if (key == Key.esc):
        print("\"Esc\" pressed, exiting...")
    elif (key == Key.tab):
        os.system('cls')
        global ctr
        print("Iteration: " + str(ctr))
        ctr+=1
        for x in range(ROWS):
            for y in range(COLS):
                if (arr[x][y] == 1): # if alive
                    liveneighbours = getLiveNeighbourCount(arr, x, y)
                    if (liveneighbours > 3):
                        arr[x][y] = 0 # die, overpopulation
                    elif (liveneighbours == 2 or liveneighbours == 3):
                        arr[x][y] = 1 # live on
                    elif (liveneighbours < 2):
                        arr[x][y] = 0 # die, underpopulation
                else: # if dead
                    if (getLiveNeighbourCount(arr, x, y) == 3):
                        arr[x][y] = 1 # alive, reproduction
                printcell(arr[x][y])
            print("")

def on_release(key):
    if key == Key.esc:
        return False
    elif key == Key.tab:
        pass

#----Main----#

# for randomly generating cells
# for i in range(ROWS):
#     for j in range(COLS):
#         arr[i][j] = 0 #random.randint(0, 1)
#         printcell(arr[i][j])
#     print("")

print("-----------------Welcome to Conway's Game of Life-----------------")
print("Open the \"input.txt\" file in the same folder\nEvery \"1\" is a live cell and \"0\" is a dead cell\nYou can customize the initial cells in that file.\nA sample input is already in the file.")
print("\nPress Enter to load file")
with Listener(on_press=on_init_press, on_release=on_init_release) as init_listener:
    init_listener.join()

print("World initialized... Starting simulation...\nPress \"Tab\" to step\nPress \"Esc\" to exit")
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()