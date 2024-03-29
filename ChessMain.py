'''
This is our main driver file. It will be responsible for handling input and displaying thu current GameState object.
'''

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512 #400 IS ANOTHER OPTION
DIMENSION = 8#dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION # 64 - the width of the square
MAX_FPS = 15
IMAGES= {}






'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK' , 'wQ' , 'bp', 'bR', 'bN', 'bB', 'bK' , 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))        
    #Note: we can acces an image by saying 'IMAGES['wp'];
    # formula de incarcat imaginea -->   IMAGES[piece] = p.image.load("path-ul imaginii")
    # formula de scalare           -->   p.transform.scale( obiectul , (dimensiunea y, dimensiunea x))
    





'''
The main driver for our code. This will handle user input and updating the graphics
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves() # if moveMade is true then validMoves will generate the new moves in the current game situation
    moveMade = False #flag variable for when a move is made
    

    loadImages() #only do this once, before the while loop
    running = True
    sqSelected = () #no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] # keep track of the player clicks (two tuples: [(6,5),(4, 4)])


    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x, y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): #the user clicked the same square
                    sqSelected = () #deselect
                    playerClicks = [] #clear player clicks
                else:
                    sqSelected=(row,col)
                    playerClicks.append(sqSelected) #append for both 1st and 2nd click
                if len(playerClicks) == 2: #after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = () #reset user clicks
                            playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False



               
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()








'''
Responsible for all the graphics within a current game state.
'''

def drawGameState(screen, gs):
    drawBoard(screen) #draw squares on the board
    #add in piece highlighting or move suggestions (later)
    drawPieces(screen, gs.board) #draw pieces on top of those squares


'''
Draw the squares on the board. The top left square is always light.
'''

def drawBoard(screen):
    colors= [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Draw the pieces on the board using the current GameState.board
'''

def drawPieces(screen, board):
    pass
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))    # aici se pune poza pe screen    p.Rect(pozitiex, pozittiay, lungime, latime)







if __name__ == "__main__":
    main()