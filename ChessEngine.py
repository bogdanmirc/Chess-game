'''
This class is responsible for storing all the information about the current state of a chess game. It will also be
 responsible for determining the valid moves at the current state. it will also keep a move log.
'''

class GameState():
   
    def __init__(self):
        #board is an 8x8 2s list, each element of the list has 2 characters.
        #The first character represents the color of the piece, 'b' or 'w'
        #The second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N' OR 'P'
        #"--" - represents an emty space with no piece.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR",],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["--", "--", "--", "--", "--", "--", "--", "--",],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp",],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR",]
        ]
        self.moveFunction = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = () #coordinates for the square where en passant capture is possible
        
        
    '''
    Takes a Move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passant)
    '''

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swap players
        #update the king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
        
        #pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        #enpassant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--' #capturing the pawn
            
        #update enpassantPossible variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: #only on 2 square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()
    
    '''
    Undo the last move made
    '''

    def undoMove(self):
        if len(self.moveLog) != 0: #make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol]= move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCapture
            self.whiteToMove = not self.whiteToMove #switch turns back
            #update the king's position if needed
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            #undo en passant 
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--' #leave landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            #undo a 2 square pawn advance
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()





    '''
    All moves considering checks
    '''

    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        #1. ) generate all possible moves
        moves = self.getAllPossibleMoves() #for now we will not worry about checks
        #2. ) for each move, make a move
        for i in range(len(moves)-1, -1, -1): #when removing from a list go backwards through that list
            self.makeMove(moves[i])
            #3. ) generate all opponent's moves
            #4. ) for each of your opponent's moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])  #5. ) if they do attack your king, not a valid move
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0: #either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.enpassantPossible = tempEnpassantPossible
        return moves


    '''
    Determine if the current player is in check
    '''
    
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


    '''
    Determine if the enemy can attack the square r, c
    '''


    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch to opponent's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #square is under attack
                return True
        return False
        
    

    

    '''
    All moves without considering checks
    '''

    def getAllPossibleMoves(self):
        
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #nomber of cols in given row
                turn = self.board[r][c][0] # first character in the element ex.  "bN" --> b
                if (turn =='w' and self. whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1] # second character in the element ex.  "bN" --> N    Type of piece
                    self.moveFunction[piece](r, c, moves) #calls the appropriate move function based on piece type
        return moves









    ''' 
    Get all the pawn moves for the pawn located at row, col and add these moves to the lsit
    '''

    def getPawnMoves(self, r, c, moves):
        
        
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == "--": #1 square pawn advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0: #captures to the left
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, isEnpassantMove = True))

            if c+1 <= 7: #captures to the right
                if self.board[r-1][c+1][0] == 'b': #enemy piece to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, isEnpassantMove = True))

        else:  # black pawn moves
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c), (r+2, c), self.board))
            if c-1 >=0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c-1), self.board, isEnpassantMove = True))
            if c+1<=7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c+1), self.board, isEnpassantMove = True))
        
        #add pawn promotions later









    '''
    Get all the rook moves for the rook located at row, col and add these moves to the lsit
    '''

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1,0), (0,1)) # up, left, down, right  
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #emty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #friendly piece invalid
                        break
                else: #off board
                    break

    





    '''
    Get all the knight moves for the Knight located at row, col and add these moves to the lsit
    '''

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow <8 and 0 <= endCol <8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #not an ally piece(empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))







    '''
    Get all the bishop moves for the bishop located at row, col and add these moves to the lsit
    '''

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) #4 diagonals
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8): #bishop can move max 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <8 and 0 <= endCol < 8: #is it on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #emty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #friendly piece invalid
                        break
                else: #off board
                    break






    '''
    Get all the queen moves for the queen located at row, col and add these moves to the lsit
    '''

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r,c, moves)
        self.getBishopMoves(r, c, moves)
    
    '''
    Get all the king moves for the king located at row, col and add these moves to the lsit
    '''







    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0<= endRow <8 and 0 <= endCol <8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #not an ally piece(emty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))









class Move():
    #maps keys to value

    # key : value

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0,}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7,}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    

    def __init__(self, startSq, endSq, board, isEnpassantMove =False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCapture = board[self.endRow][self.endCol]
        #pawn promotion
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)
            
        #en passant
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
       

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        

    '''
    Overriding the equals method
    '''

    def __eq__(self, other):
        
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        #you can add to make this like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]